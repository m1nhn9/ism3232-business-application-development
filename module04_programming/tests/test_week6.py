import subprocess
import sys
from pathlib import Path

from module04_programming.week6_lab import HIGH, LIMIT, process_records, records


def test_accumulator():
    total, _, _ = process_records(records)
    assert total == 3939
    assert process_records([]) == (0, [], [])


def test_flag_filter():
    expenses = [
        {"id": 1, "amount": LIMIT, "status": "Pending"},
        {"id": 2, "amount": LIMIT + 1, "status": "Pending"},
        {"id": 3, "amount": HIGH, "status": "Pending"},
        {"id": 4, "amount": HIGH + 1, "status": "Pending"},
    ]
    _, flagged, high_value = process_records(expenses)
    assert [rec["id"] for rec in flagged] == [2, 3, 4]
    assert [rec["id"] for rec in high_value] == [4]


def test_status_filter():
    expenses = [
        {"amount": 500, "status": "Pending"},
        {"amount": HIGH + 1000, "status": "Approved"},
        {"amount": HIGH + 2000, "status": "Rejected"},
    ]
    assert process_records(expenses) == (500, [], [])


def test_dict_key_access():
    assert len(records) >= 5
    assert len({rec["id"] for rec in records}) == len(records)
    for rec in records:
        assert {"id", "name", "category", "amount", "status"} <= rec.keys()
    assert records[0]["amount"] == 1200
    _, flagged, high_value = process_records(records)
    assert [rec["id"] for rec in flagged] == [1, 5]
    assert [rec["id"] for rec in high_value] == [5]


def test_summary_output(tmp_path):
    script = Path(__file__).resolve().parents[1] / "week6_lab.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    summary = "Pending total:   $3,939.00\nNeeds review:    2\nHigh-value:      1\n"
    summary_path = script.parent / "data" / "week6_summary.txt"
    assert summary_path.read_text() == summary
    assert not (tmp_path / "data").exists()
    assert result.stdout == (
        "Pending records:\n"
        "Taylor: $1,200.00\n"
        "Jordan: $450.00\n"
        "Riley: $89.00\n"
        "Alex: $2,200.00\n\n"
        f"{summary}\n"
        "Records needing review:\n"
        "  ID 1: Taylor - $1,200.00\n"
        "  ID 5: Alex - $2,200.00\n"
    )
    assert result.stderr == ""
