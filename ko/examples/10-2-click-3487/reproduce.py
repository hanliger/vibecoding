"""Reproduce Click #3487 in a fresh checkout. Requires Git and uv."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse
import hashlib
import json
import os
import subprocess

BASE = "d42f15b71757de791a5781fb179fd972da9169f5"
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--workdir", required=True, type=Path,
                    help="A new directory; existing directories are refused.")
args = parser.parse_args()
work = args.workdir.resolve()
if work.exists():
    raise SystemExit(f"Refusing to overwrite existing directory: {work}")
work.mkdir(parents=True)
repo = work / "click"
logs = work / "logs"
logs.mkdir()
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
env.pop("PYTHONPATH", None)
records = []


def run(label, command, expected=0, cwd=None, input_text=None):
    command = [str(x) for x in command]
    proc = subprocess.run(command, cwd=cwd or work, env=env,
                          text=True, encoding="utf-8", errors="replace",
                          capture_output=True, input=input_text)
    output = proc.stdout + proc.stderr
    (logs / f"{label}.txt").write_text(output, encoding="utf-8")
    records.append({"label": label, "argv": command,
                    "cwd": str(cwd or work), "exit_code": proc.returncode})
    print(f"{label}: exit {proc.returncode}")
    if proc.returncode != expected:
        raise RuntimeError(f"Unexpected exit code. See {logs / (label + '.txt')}")
    return output


run("clone", ["git", "clone", "https://github.com/pallets/click.git", repo])
run("checkout", ["git", "checkout", "--detach", BASE], cwd=repo)
run("venv", ["uv", "venv", "--python", "3.14.5", ".venv"], cwd=repo)
py = repo / (".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python")
run("install", ["uv", "pip", "install", "--python", py, "-e", ".",
                "pytest==9.2.0", "colorama==0.4.6", "iniconfig==2.3.1",
                "packaging==26.3", "pluggy==1.7.0", "pygments==2.21.0"], cwd=repo)
environment = run("environment", [py, "-c",
    'import sys,platform,click,importlib.metadata as m; '
    'print(sys.version); print(platform.platform()); '
    'print("click",m.version("click")); print("pytest",m.version("pytest")); '
    'print("source",click.__file__)'], cwd=repo)
test_hash = hashlib.sha256((HERE / "test_echo_3487.py").read_bytes()).hexdigest()
for phase in ("before", "after"):
    if phase == "after":
        run("apply-check", ["git", "apply", "--check", HERE / "fix.patch"], cwd=repo)
        run("apply", ["git", "apply", HERE / "fix.patch"], cwd=repo)
    if phase == "before":
        source = repo / "src/click/utils.py"
        line = next(i for i, text in enumerate(source.read_text(encoding="utf-8").splitlines(), 1)
                    if "out = out or" in text)
        commands = (f"b {source.as_posix()}:{line}\nc\n"
                    'p (type(out).__name__, repr(out))\nn\n'
                    'p (type(out).__name__, repr(out))\nn\nn\n'
                    'p (type(out).__name__, repr(out))\nq\n')
        run("before-pdb", [py, "-m", "pdb", HERE / "repro.py"], cwd=repo, input_text=commands)
    run(f"{phase}-repro", [py, HERE / "repro.py"], expected=1 if phase == "before" else 0, cwd=repo)
    run(f"{phase}-matrix", [py, HERE / "matrix.py"], cwd=repo)
    run(f"{phase}-regression", [py, "-m", "pytest", HERE / "test_echo_3487.py", "-q", "--tb=short"],
        expected=1 if phase == "before" else 0, cwd=repo)
    run(f"{phase}-shared-10-1", [py, "-m", "pytest", HERE / "shared-10-1/test_echo_contract.py",
        HERE / "shared-10-1/test_emit.py", "-q", "--tb=short"],
        expected=1 if phase == "before" else 0, cwd=repo)
    run(f"{phase}-existing-utils", [py, "-m", "pytest", "tests/test_utils.py", "-q", "--tb=short", "-rs"], cwd=repo)
    assert hashlib.sha256((HERE / "test_echo_3487.py").read_bytes()).hexdigest() == test_hash
run("final-diff", ["git", "diff", "--", "src/click/utils.py"], cwd=repo)
metadata = {"date_kst": datetime.now(timezone(timedelta(hours=9))).isoformat(),
            "base_commit": BASE, "test_sha256": test_hash,
            "environment": environment, "commands": records,
            "authoring_tool": "Codex desktop, app build not exposed", "authoring_model": "gpt-6.1-sol (session identity)",
            "interpretation": "Known-bug reproduction, not an independent agent discovery benchmark."}
(logs / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Completed. Evidence: {logs}")
