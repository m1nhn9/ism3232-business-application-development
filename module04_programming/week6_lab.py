# module04_programming/week6_lab.py
# Author: Minh Nguyen

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

records = [
    {
        "id": 1,
        "name": "Taylor",
        "category": "Travel",
        "amount": 1200,
        "status": "Pending",
    },
    {
        "id": 2,
        "name": "Jordan",
        "category": "Equipment",
        "amount": 450,
        "status": "Pending",
    },
    {
        "id": 3,
        "name": "Morgan",
        "category": "Software",
        "amount": 3500,
        "status": "Approved",
    },
    {"id": 4, "name": "Riley", "category": "Travel", "amount": 89, "status": "Pending"},
    {
        "id": 5,
        "name": "Alex",
        "category": "Equipment",
        "amount": 2200,
        "status": "Pending",
    },
]

LIMIT = 1000
HIGH = 2000


def process_records(records):
    """Total pending expenses and apply the two review thresholds."""
    total = 0
    flagged = []
    high_value = []

    for rec in records:
        if rec["status"] == "Pending":
            total += rec["amount"]
            if rec["amount"] > LIMIT:
                flagged.append(rec)
            if rec["amount"] > HIGH:
                high_value.append(rec)

    return total, flagged, high_value


if __name__ == "__main__":
    print("Pending records:")
    for rec in records:
        if rec["status"] == "Pending":
            print(f"{rec['name']}: ${rec['amount']:,.2f}")

    total, flagged, high_value = process_records(records)
    lines = [
        f"Pending total:   ${total:,.2f}",
        f"Needs review:    {len(flagged)}",
        f"High-value:      {len(high_value)}",
    ]

    print()
    for line in lines:
        print(line)

    DATA_DIR.mkdir(exist_ok=True)
    summary_path = DATA_DIR / "week6_summary.txt"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\nRecords needing review:")
    for rec in flagged:
        print(f"  ID {rec['id']}: {rec['name']} - ${rec['amount']:,.2f}")
