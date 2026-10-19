import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


BASELINE = "f2e7be6fa6293099c1d4a02c945b9f1432831119"
SKILLS = (
    "refactoring-guru-code-smells",
    "refactoring-guru-design-patterns",
    "refactoring-guru-refactoring",
)
ARMS = (
    ("cedar", "baseline", "gpt-6-sol"),
    ("willow", "enriched", "gpt-6-sol"),
    ("birch", "enriched", "gpt-6-luna"),
    ("maple", "baseline", "gpt-6-luna"),
)
GUIDANCE = """# Working on this project

Use the bundled skills for the requested work. Read each relevant SKILL.md,
then its relevant local references, with `python3 read_skill.py <path>`.
Paths are relative to .skills, for example
`python3 read_skill.py refactoring-guru-refactoring/SKILL.md`.
The reader prints the document and records local documentation access.
Use only this project and standard Python. Network access is unavailable.
Keep .skills, read_skill.py, AGENTS.md, and request.txt unchanged.
Follow the file permissions in request.txt. Do not start other agents.
"""
READER = '''import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
folder = root / ".skills"
path = (folder / sys.argv[1]).resolve()
if not path.is_relative_to(folder) or not path.is_file():
    raise SystemExit("Choose a file within .skills")
payload = path.read_bytes()
activity = root / ".activity"
activity.mkdir(exist_ok=True)
with (activity / "reading.jsonl").open("a") as stream:
    stream.write(json.dumps({"path": str(path.relative_to(folder)), "sha256": hashlib.sha256(payload).hexdigest()}) + "\\n")
print(payload.decode("utf-8"))
'''


def baseline_files(repo, revision):
    names = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", revision, "--", *SKILLS],
        cwd=repo, text=True,
    ).splitlines()
    if not names:
        raise ValueError("No baseline skill files at the pinned revision")
    return {
        name: subprocess.check_output(["git", "show", f"{revision}:{name}"], cwd=repo)
        for name in names
    }


def prepare(repo, inputs, destination, revision):
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("Use an empty output directory to preserve existing work")
    original = baseline_files(repo, revision)
    enriched = {
        str(path.relative_to(repo)): path.read_bytes()
        for skill in SKILLS for path in (repo / skill).rglob("*") if path.is_file()
    }
    manifest = {"baseline": revision, "arms": [], "documents": {}}
    for label, version, model in ARMS:
        project = destination / label
        project.mkdir(parents=True)
        for name in ("strategy.py", "refactoring.py", "audit.py", "request.txt"):
            shutil.copy2(inputs / name, project / name)
        (project / "AGENTS.md").write_text(GUIDANCE)
        (project / "read_skill.py").write_text(READER)
        package = original if version == "baseline" else enriched
        hashes = {}
        for name, content in package.items():
            target = project / ".skills" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            hashes[name] = hashlib.sha256(content).hexdigest()
        immutable = {
            name: hashlib.sha256((project / name).read_bytes()).hexdigest()
            for name in ("AGENTS.md", "read_skill.py", "request.txt", "audit.py")
        }
        manifest["arms"].append(dict(label=label, variant=version, model=model,
                                     effort="high", immutable=immutable))
        manifest["documents"][label] = hashes
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, default=Path(__file__).parent / "input")
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--baseline", default=BASELINE)
    args = parser.parse_args()
    manifest = prepare(args.repo.resolve(), args.inputs.resolve(),
                       args.destination.resolve(), args.baseline)
    print(json.dumps({"projects": [arm["label"] for arm in manifest["arms"]],
                      "baseline": manifest["baseline"]}, indent=2))
