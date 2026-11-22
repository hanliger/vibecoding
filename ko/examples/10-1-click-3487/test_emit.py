import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from emit import emit


def test_file_argument(tmp_path):
    target = tmp_path / "out.bin"
    result = CliRunner().invoke(emit, [str(target)])
    assert result.exit_code == 0, repr(result.exception)
    assert target.read_bytes() == b"\n"


def test_file_from_shell(tmp_path):
    target = tmp_path / "out.bin"
    script = Path(__file__).with_name("emit.py")
    result = subprocess.run(
        [sys.executable, str(script), str(target)], capture_output=True
    )
    assert result.returncode == 0, result.stderr
    assert target.read_bytes() == b"\n"
