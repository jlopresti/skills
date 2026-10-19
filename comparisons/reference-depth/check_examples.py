import argparse
import copy
import json
from pathlib import Path
import re


PAGES = {
    "strategy": "refactoring-guru-design-patterns/references/strategy.md",
    "long-method": "refactoring-guru-code-smells/references/long-method.md",
    "extract-method": "refactoring-guru-refactoring/references/extract-method.md",
}


def outcome(call, state):
    try:
        result = call()
        error = None
    except Exception as exc:
        result = None
        error = (type(exc).__name__, str(exc))
    return result, error, copy.deepcopy(state)


def observe(topic, namespace):
    observed = []
    if topic == "strategy":
        quote = namespace["quote_shipping"]
        for weight in (0, -1, 1, 249, 250, 251, 499, 500, 501):
            for service in ("economy", "express", "missing"):
                events = ["earlier"]
                observed.append(outcome(lambda: quote(weight, service, events), events))
        events = []
        assert quote(500, "economy", events) == 490
        assert events == ["quote:economy:490"]
    elif topic == "long-method":
        close = namespace["close_rental"]
        for member in (False, True):
            for returned in (1, 2, 3, 4, 6):
                rental = dict(status="out", start_day=2, due_day=3,
                              daily_fee_cents=75, member=member, id="R1", item="Drill")
                events = []
                def emit(receipt):
                    events.append((receipt, copy.deepcopy(rental)))
                observed.append(outcome(lambda: close(rental, returned, emit), (rental, events)))
        rental = dict(status="out", start_day=2, due_day=3,
                      daily_fee_cents=75, member=True, id="R1", item="Drill")
        receipt = close(rental, 6, lambda text: None)
        assert receipt == "Return R1\nItem: Drill\nOverdue days: 3\nFee: 1.25\nMembership allowance applied"
        assert rental["status"] == "returned" and rental["fee_cents"] == 125
        def fail(receipt):
            raise RuntimeError("printer unavailable")
        rental["status"] = "out"
        observed.append(outcome(lambda: close(rental, 6, fail), rental))
    else:
        write = namespace["write_balance"]
        for rows in ([], [{"cents": 30, "count": 2}, {"cents": 5, "count": 3}],
                     [{"cents": 30, "count": 2}, {"count": 4}]):
            events = []
            def source():
                for row in rows:
                    events.append(("yield", copy.deepcopy(row)))
                    yield row
            observed.append(outcome(lambda: write(source(), 100, events.append), events))
        events = []
        assert write(iter([{"cents": 30, "count": 2}, {"cents": 5, "count": 3}]), 100, events.append) == 175
        assert events == [{"balance_cents": 175}]
        def fail(value):
            raise RuntimeError("printer unavailable")
        observed.append(outcome(lambda: write(iter([]), 100, fail), []))
    return observed


def check(root, controls):
    result = {}
    mutations = {
        "strategy": ("return 400 +", "return 401 +"),
        "long-method": ('rental["status"] = "returned"', 'rental["status"] = "out"'),
        "extract-method": ("balance_cents = _accumulate_balance(lines, opening_cents)",
                           "balance_cents = opening_cents\n\t_accumulate_balance(lines, opening_cents)"),
    }
    for topic, relative in PAGES.items():
        path = root / relative
        blocks = re.findall(r"```python\n(.*?)\n```", path.read_text(), re.S)
        if len(blocks) != 2:
            raise ValueError(f"{relative} must contain two Python example blocks")
        before, after = {}, {}
        exec(compile(blocks[0], str(path) + ":before", "exec"), before)
        exec(compile(blocks[1], str(path) + ":after", "exec"), after)
        expected = observe(topic, before)
        actual = observe(topic, after)
        assert actual == expected, (topic, expected, actual)
        result[topic] = {"contract": "PASS", "observations": len(actual)}
        if controls:
            old, new = mutations[topic]
            if old not in blocks[1]:
                raise ValueError(f"Missing fault-control edit for {topic}")
            broken = {}
            exec(compile(blocks[1].replace(old, new), str(path) + ":fault", "exec"), broken)
            try:
                broken_result = observe(topic, broken)
            except AssertionError:
                rejected = True
            else:
                rejected = broken_result != expected
            assert rejected, f"Fault control was not detected for {topic}"
            result[topic]["fault_control"] = "rejected behavioral mismatch"
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    print(json.dumps(check(args.root, args.controls), indent=2))
