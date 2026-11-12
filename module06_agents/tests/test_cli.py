import subprocess
import sys
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]


def run_cli(script, messages=""):
    return subprocess.run(
        [sys.executable, str(MODULE / script)],
        input=messages,
        text=True,
        capture_output=True,
        check=True,
        cwd=MODULE,
    ).stdout


def test_two_bots_output_matches_the_exercise():
    assert run_cli("two_bots.py") == (
        "Sunny 5\nRiver 2\n"
        "Hello! How can I help you today?\n"
        "Hello! How can I help you today?\n"
        "You are cheerful and brief.\n"
        "You are formal and detailed.\n"
    )
