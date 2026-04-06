"""Future utility wrapper for running iverilog checks in CI/local workflows."""

from pathlib import Path
import subprocess


def run_iverilog(verilog_file: Path) -> tuple[int, str, str]:
    process = subprocess.run(
        ["iverilog", str(verilog_file)],
        capture_output=True,
        text=True,
        check=False,
    )
    return process.returncode, process.stdout, process.stderr
