import argparse
import importlib.util
import json
from pathlib import Path
import sys


sys.dont_write_bytecode = True


def observe(source):
    spec = importlib.util.spec_from_file_location("rendering", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    events = []

    class Style(str):
        def __eq__(self, other):
            events.append(["equals", other])
            if sum(row[0] == "equals" for row in events) == 2:
                raise RuntimeError("comparison failed")
            return str.__eq__(self, other)

    def items():
        for name in ("first", "second"):
            events.append(["yield", name])
            yield {"name": name, "sku": name}

    def emit(value):
        events.append(["emit", value])

    try:
        result = module.render_batch(items(), Style("label"), emit)
        error = None
    except Exception as exc:
        result = None
        error = [type(exc).__name__, str(exc)]
    return {"result": result, "error": error, "events": events}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("projects", type=Path, nargs="+")
    args = parser.parse_args()
    original = observe(args.original)
    assert original["error"] == ["RuntimeError", "comparison failed"]
    assert sum(row[0] == "emit" for row in original["events"]) == 1
    reports = {}
    for project in args.projects:
        actual = observe(project / "strategy.py")
        reports[project.name] = {"matches_original": actual == original, "observed": actual}
    print(json.dumps({"original": original, "projects": reports}, indent=2))
    raise SystemExit(0 if all(row["matches_original"] for row in reports.values()) else 1)
