#!/usr/bin/env python3
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "input"
AUDIT_SHA256 = "a86f43d2d6474e0680eb025e3e3402349630ac921a15fd3f266a1c8b1dc626b0"
sys.dont_write_bytecode = True


class CallbackFault(Exception):
    pass


class StreamFault(Exception):
    pass


class EventFault(Exception):
    pass


class ChargeFault(Exception):
    pass


def invoke(function, *args):
    try:
        return function(*args), None
    except Exception as error:
        return None, error


def error_name(error):
    return None if error is None else type(error).__name__


def load_function(project, filename, public_name):
    path = project / filename
    module = types.ModuleType(filename[:-3])
    module.__file__ = str(path)
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
    function = getattr(module, public_name)
    if not callable(function):
        raise TypeError("public entry point is not callable")
    return function


def observe_strategy(render_batch):
    observations = {}
    for style in ("label", "slug"):
        items = [
            {"name": "  olive OIL  ", "sku": "rA2"},
            {"name": "Crème Brûlée", "sku": "S4"},
        ]
        emitted = []
        result, error = invoke(render_batch, items, style, emitted.append)
        observations["strategy." + style] = {
            "result": result, "emitted": emitted, "source": items,
            "error": error_name(error),
        }

    trace = []

    def empty():
        trace.append("opened")
        yield from ()

    emitted = []
    result, error = invoke(render_batch, empty(), "absent", emitted.append)
    observations["strategy.empty_unknown"] = {
        "result": result, "emitted": emitted, "trace": trace,
        "error": error_name(error),
    }

    trace = []
    rows = [{"name": "FIRST BOX", "sku": "A"}, {"name": "old name", "sku": "B"}]

    def stream():
        for row in rows:
            trace.append(["yield", row["sku"]])
            yield row
            trace.append(["resume", row["sku"]])

    emitted = []
    result, error = invoke(render_batch, stream(), "absent", emitted.append)
    observations["strategy.unknown"] = {
        "result": result, "emitted": emitted, "trace": list(trace),
        "error": error_name(error),
    }

    trace.clear()

    def emit(text):
        trace.append(["emit", text])
        if len(trace) == 2:
            rows[1]["name"] = "fresh crate"

    result, error = invoke(render_batch, stream(), "slug", emit)
    observations["strategy.interleaving"] = {
        "result": result, "trace": list(trace), "error": error_name(error),
    }

    trace.clear()
    marker = CallbackFault()

    def stop(text):
        trace.append(["emit", text])
        raise marker

    result, error = invoke(render_batch, stream(), "slug", stop)
    observations["strategy.callback_stop"] = {
        "result": result, "trace": list(trace), "error": error_name(error),
        "same_error": error is marker,
    }

    trace.clear()
    marker = StreamFault()

    def broken_stream():
        trace.append("opened")
        yield rows[0]
        trace.append("resumed")
        raise marker

    emitted = []
    result, error = invoke(render_batch, broken_stream(), "slug", emitted.append)
    observations["strategy.stream_failure"] = {
        "result": result, "emitted": emitted, "trace": list(trace),
        "error": error_name(error), "same_error": error is marker,
    }

    trace.clear()

    def unavailable_stream():
        trace.append("opened")
        raise marker
        yield

    emitted = []
    result, error = invoke(render_batch, unavailable_stream(), "absent", emitted.append)
    observations["strategy.first_pull_failure"] = {
        "result": result, "emitted": emitted, "trace": list(trace),
        "error": error_name(error), "same_error": error is marker,
    }
    return observations


def summarize_settle(result, error, rows, events):
    outcome = {
        "error": error_name(error), "events": list(events),
        "rows": [dict(row) for row in rows],
    }
    if error is None:
        try:
            total, accepted = result
            outcome["total"] = total
            outcome["accepted"] = [dict(row) for row in accepted]
            outcome["aliases"] = [
                next((i for i, original in enumerate(rows) if row is original), None)
                for row in accepted
            ]
        except Exception as malformed:
            outcome["return_error"] = error_name(malformed)
    return outcome


class ObservedRow(dict):
    def __init__(self, tag, trace, values, failure=None):
        super().__init__(values)
        self.tag = tag
        self.trace = trace
        self.failure = failure

    def __getitem__(self, key):
        self.trace.append(["read", self.tag, key])
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        self.trace.append(["write", self.tag, key, value])
        if key == "charged" and self.failure is not None:
            raise self.failure
        super().__setitem__(key, value)


class ObservedEvents(list):
    def __init__(self, trace, failure=None):
        super().__init__()
        self.trace = trace
        self.failure = failure

    def append(self, event):
        self.trace.append(["event", event])
        if isinstance(event, tuple) and event[0] == "total" and self.failure is not None:
            raise self.failure
        super().append(event)


def observe_refactoring(settle):
    observations = {}
    rows = [
        {"sku": "A", "enabled": True, "price": 5, "units": 3},
        {"sku": "B", "enabled": False, "price": 99, "units": 2},
        {"sku": "C", "enabled": True, "price": 2, "units": 4},
    ]
    events = []
    result, error = invoke(settle, (row for row in rows), 7, events)
    observations["refactoring.mixed"] = summarize_settle(result, error, rows, events)

    events = []
    result, error = invoke(settle, iter(()), 13, events)
    observations["refactoring.empty"] = summarize_settle(result, error, [], events)

    for name, kind in (("order", None), ("preparation_error", "units"),
                       ("total_event_error", "event"), ("charge_error", "charge")):
        trace = []
        marker = EventFault() if kind == "event" else ChargeFault() if kind == "charge" else None
        rows = [
            ObservedRow("A", trace, {"sku": "A", "enabled": True, "price": 2, "units": 3},
                        marker if kind == "charge" else None),
            ObservedRow("B", trace, {"sku": "B", "enabled": False}),
        ]
        if kind == "units":
            rows[1] = ObservedRow("B", trace, {"sku": "B", "enabled": True, "price": 4})
        events = ObservedEvents(trace, marker if kind == "event" else None)

        def stream():
            for row in rows:
                trace.append(["yield", row.tag])
                yield row
                trace.append(["resume", row.tag])
            trace.append("exhausted")

        result, error = invoke(settle, stream(), 11, events)
        outcome = summarize_settle(result, error, rows, events)
        outcome["trace"] = trace
        if marker is not None:
            outcome["same_error"] = error is marker
        observations["refactoring." + name] = outcome

    trace = []
    rows = [ObservedRow("A", trace, {"enabled": True, "price": 2, "units": 3})]
    events = ObservedEvents(trace)
    result, error = invoke(settle, iter(rows), 11, events)
    observations["refactoring.missing_sku"] = {
        **summarize_settle(result, error, rows, events), "trace": trace,
    }

    row = {"sku": "R", "enabled": True, "price": 3, "units": 2}
    rows = [row]
    events = []
    result, error = invoke(settle, (value for value in (row, row)), 1, events)
    observations["refactoring.shared_row"] = summarize_settle(result, error, rows, events)
    return observations


UNCHANGED_ITEMS = [
    {"name": "  olive OIL  ", "sku": "rA2"},
    {"name": "Crème Brûlée", "sku": "S4"},
]
MIXED_ROWS = [
    {"sku": "A", "enabled": True, "price": 5, "units": 3, "charged": True},
    {"sku": "B", "enabled": False, "price": 99, "units": 2},
    {"sku": "C", "enabled": True, "price": 2, "units": 4, "charged": True},
]
ORDER_ROWS = [
    {"sku": "A", "enabled": True, "price": 2, "units": 3},
    {"sku": "B", "enabled": False},
]
ORDER_TRACE = [
    ["event", "start"], ["yield", "A"], ["read", "A", "sku"],
    ["event", ["item", "A"]], ["read", "A", "enabled"],
    ["read", "A", "price"], ["read", "A", "units"], ["resume", "A"],
    ["yield", "B"], ["read", "B", "sku"], ["event", ["item", "B"]],
    ["read", "B", "enabled"], ["resume", "B"], "exhausted",
]
ORDER_EVENTS = ["start", ["item", "A"], ["item", "B"]]
CHARGED_A = {**ORDER_ROWS[0], "charged": True}
EXPECTED = {
    "strategy.label": {
        "result": ["Olive Oil / RA2", "Crème Brûlée / S4"],
        "emitted": ["Olive Oil / RA2", "Crème Brûlée / S4"],
        "source": UNCHANGED_ITEMS, "error": None,
    },
    "strategy.slug": {
        "result": ["olive-oil:ra2", "crème-brûlée:s4"],
        "emitted": ["olive-oil:ra2", "crème-brûlée:s4"],
        "source": UNCHANGED_ITEMS, "error": None,
    },
    "strategy.empty_unknown": {"result": [], "emitted": [], "trace": ["opened"], "error": None},
    "strategy.unknown": {
        "result": None, "emitted": [], "trace": [["yield", "A"]], "error": "ValueError",
    },
    "strategy.interleaving": {
        "result": ["first-box:a", "fresh-crate:b"], "error": None,
        "trace": [["yield", "A"], ["emit", "first-box:a"], ["resume", "A"],
                  ["yield", "B"], ["emit", "fresh-crate:b"], ["resume", "B"]],
    },
    "strategy.callback_stop": {
        "result": None, "error": "CallbackFault", "same_error": True,
        "trace": [["yield", "A"], ["emit", "first-box:a"]],
    },
    "strategy.stream_failure": {
        "result": None, "emitted": ["first-box:a"], "trace": ["opened", "resumed"],
        "error": "StreamFault", "same_error": True,
    },
    "strategy.first_pull_failure": {
        "result": None, "emitted": [], "trace": ["opened"],
        "error": "StreamFault", "same_error": True,
    },
    "refactoring.mixed": {
        "error": None, "events": ["start", ["item", "A"], ["item", "B"], ["item", "C"], ["total", 30]],
        "rows": MIXED_ROWS, "total": 30, "accepted": [MIXED_ROWS[0], MIXED_ROWS[2]], "aliases": [0, 2],
    },
    "refactoring.empty": {
        "error": None, "events": ["start", ["total", 13]], "rows": [],
        "total": 13, "accepted": [], "aliases": [],
    },
    "refactoring.order": {
        "error": None, "events": ORDER_EVENTS + [["total", 17]], "rows": [CHARGED_A, ORDER_ROWS[1]],
        "total": 17, "accepted": [CHARGED_A], "aliases": [0],
        "trace": ORDER_TRACE + [["event", ["total", 17]], ["write", "A", "charged", True]],
    },
    "refactoring.preparation_error": {
        "error": "KeyError", "events": ORDER_EVENTS,
        "rows": [ORDER_ROWS[0], {"sku": "B", "enabled": True, "price": 4}],
        "trace": ORDER_TRACE[:12] + [["read", "B", "price"], ["read", "B", "units"]],
    },
    "refactoring.total_event_error": {
        "error": "EventFault", "events": ORDER_EVENTS, "rows": ORDER_ROWS, "same_error": True,
        "trace": ORDER_TRACE + [["event", ["total", 17]]],
    },
    "refactoring.charge_error": {
        "error": "ChargeFault", "events": ORDER_EVENTS + [["total", 17]],
        "rows": ORDER_ROWS, "same_error": True,
        "trace": ORDER_TRACE + [["event", ["total", 17]], ["write", "A", "charged", True]],
    },
    "refactoring.missing_sku": {
        "error": "KeyError", "events": ["start"],
        "rows": [{"enabled": True, "price": 2, "units": 3}],
        "trace": [["event", "start"], ["read", "A", "sku"]],
    },
    "refactoring.shared_row": {
        "error": None, "events": ["start", ["item", "R"], ["item", "R"], ["total", 13]],
        "rows": [{"sku": "R", "enabled": True, "price": 3, "units": 2, "charged": True}],
        "total": 13,
        "accepted": [{"sku": "R", "enabled": True, "price": 3, "units": 2, "charged": True}] * 2,
        "aliases": [0, 0],
    },
}


def observe(project):
    data = {}
    for filename, public_name, observer in (
        ("strategy.py", "render_batch", observe_strategy),
        ("refactoring.py", "settle", observe_refactoring),
    ):
        try:
            function = load_function(project, filename, public_name)
            data.update(observer(function))
        except Exception as error:
            data["load." + filename] = {"error": error_name(error), "detail": str(error)}
    return json.loads(json.dumps(data))


def worker(project):
    try:
        process = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--observe", str(project)],
            capture_output=True, text=True, timeout=15, cwd=str(project),
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, {"kind": type(error).__name__, "detail": str(error)}
    if process.returncode:
        return None, {"kind": "WorkerExit", "code": process.returncode, "stderr": process.stderr}
    try:
        return json.loads(process.stdout), None
    except ValueError as error:
        return None, {"kind": "WorkerJSON", "detail": str(error)}


def mismatch(check, expected, actual, category="contract"):
    return {"check": check, "category": category, "expected": expected, "actual": actual}


def differences(expected, actual, category="contract"):
    failures = []
    for case, fields in expected.items():
        if case not in actual:
            failures.append(mismatch(case, fields, "MISSING", category))
            continue
        for field in sorted(set(fields) | set(actual[case])):
            want = fields.get(field, "MISSING")
            got = actual[case].get(field, "MISSING")
            if want != got:
                failures.append(mismatch(case + "." + field, want, got, category))
    for case in sorted(set(actual) - set(expected)):
        failures.append(mismatch(case, "ABSENT", actual[case], category))
    return failures


def inspect_project(project, baseline, require_notes=True):
    failures = []
    for filename in ("strategy.py", "refactoring.py", "audit.py"):
        try:
            present = (project / filename).is_file()
        except OSError as error:
            failures.append(mismatch("artifacts." + filename, "readable regular file",
                                     error_name(error), "artifact"))
        else:
            if not present:
                failures.append(mismatch("artifacts." + filename, "regular file", "MISSING", "artifact"))
    notes = project / "notes.md"
    if require_notes:
        try:
            valid_notes = notes.is_file() and notes.stat().st_size > 0
        except OSError as error:
            failures.append(mismatch("artifacts.notes.md", "readable nonempty regular file",
                                     error_name(error), "artifact"))
        else:
            if not valid_notes:
                failures.append(mismatch("artifacts.notes.md", "nonempty regular file", "MISSING_OR_EMPTY", "artifact"))
    audit = project / "audit.py"
    try:
        if audit.is_file():
            digest = hashlib.sha256(audit.read_bytes()).hexdigest()
            if digest != AUDIT_SHA256:
                failures.append(mismatch("audit.sha256", AUDIT_SHA256, digest, "artifact"))
    except OSError as error:
        failures.append(mismatch("audit.read", "readable file", error_name(error), "artifact"))
    observations, error = worker(project)
    if error:
        failures.append(mismatch("execution", "completed observer", error, "execution"))
    else:
        failures.extend(differences(EXPECTED, observations))
        if baseline is not None:
            failures.extend(differences(baseline, observations, "baseline"))
    return failures, observations


LOST_TOTAL = '''def prepare(rows, total, events):
    accepted = []
    for row in rows:
        events.append(("item", row["sku"]))
        if row["enabled"]:
            total += row["price"] * row["units"]
            accepted.append(row)
    return accepted


def settle(rows, fee, events):
    events.append("start")
    total = fee
    accepted = prepare(rows, total, events)
    events.append(("total", total))
    for row in accepted:
        row["charged"] = True
    return total, accepted
'''


def run_controls(baseline):
    outcomes = []
    original_strategy = (SOURCE / "strategy.py").read_text(encoding="utf-8")
    original_refactoring = (SOURCE / "refactoring.py").read_text(encoding="utf-8")
    eager_strategy = original_strategy.replace("        emit(text)\n", "").replace(
        "    return rendered\n", "    for text in rendered:\n        emit(text)\n    return rendered\n")
    eager_style = original_strategy.replace(
        "    rendered = []\n",
        "    if style not in ('label', 'slug'):\n        raise ValueError('unknown style')\n    rendered = []\n")
    plans = (
        ("missing_artifact", None, None, "artifacts.notes.md"),
        ("lost_outer_total", None, LOST_TOTAL, "refactoring.mixed.total"),
        ("copied_rows", None, original_refactoring.replace("accepted.append(row)", "accepted.append(dict(row))"),
         "refactoring.mixed.aliases"),
        ("changed_interleaving", eager_strategy, None, "strategy.interleaving.trace"),
        ("eager_style_rejection", eager_style, None, "strategy.empty_unknown.error"),
    )
    with tempfile.TemporaryDirectory(prefix="reference-controls-") as temporary:
        directory = Path(temporary)
        for name, strategy_source, refactoring_source, intended in plans:
            project = directory / name
            project.mkdir()
            for filename in ("strategy.py", "refactoring.py", "audit.py"):
                shutil.copyfile(SOURCE / filename, project / filename)
            if name != "missing_artifact":
                (project / "notes.md").write_text("Observations de maintenance.\n", encoding="utf-8")
            if strategy_source is not None:
                (project / "strategy.py").write_text(strategy_source, encoding="utf-8")
            if refactoring_source is not None:
                (project / "refactoring.py").write_text(refactoring_source, encoding="utf-8")
            failures, _ = inspect_project(project, baseline)
            intended_failures = [failure for failure in failures if failure["check"] == intended
                                 and failure["category"] != "baseline"]
            accidental_errors = [failure for failure in failures if failure["category"] == "execution"
                                 or failure["check"].startswith("load.")]
            outcomes.append({
                "name": name, "intended_check": intended,
                "passed": bool(intended_failures) and not accidental_errors,
                "intended_evidence": intended_failures, "mismatches": failures,
            })
    return outcomes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path, nargs="?")
    parser.add_argument("--source-only", action="store_true", help="omit only the notes.md deliverable check")
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--observe", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.observe is not None:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            observations = observe(args.observe.resolve())
        print(json.dumps(observations, ensure_ascii=False))
        return 0
    if args.project is None:
        parser.error("a project directory is required")
    project = args.project.resolve()
    baseline, baseline_error = worker(SOURCE)
    baseline_failures = ([mismatch("baseline.execution", "completed observer", baseline_error, "instrument")]
                         if baseline_error else differences(EXPECTED, baseline, "instrument"))
    failures, observations = inspect_project(project, baseline, not args.source_only)
    failures = baseline_failures + failures
    controls = run_controls(baseline) if args.controls and not baseline_failures else []
    failed_controls = [item["name"] for item in controls if not item["passed"]]
    if failed_controls:
        failures.append(mismatch("controls", "all intended faults rejected", failed_controls, "instrument"))
    report = {
        "status": "PASS" if not failures else "ISSUES", "project": str(project),
        "source_only": args.source_only, "audit_sha256": AUDIT_SHA256,
        "cases": len(EXPECTED), "baseline_checked": baseline_error is None,
        "mismatches": failures, "controls": controls,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
