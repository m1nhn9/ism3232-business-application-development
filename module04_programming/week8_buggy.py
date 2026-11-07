# module04_programming/week8_buggy.py -- fixed Lab 8 debugging exercise
# Author: Minh Nguyen

records = [
    {"id": 1, "name": "Taylor", "amount": 1200},
    {"id": 2, "name": "Jordan", "amount": 450},
    {"id": 3, "name": "Morgan", "amount": 3500},
]


def get_total(records):
    total = 0
    for rec in records:
        total += rec["amount"]
    return total


def is_over_limit(amount):
    return amount > 1000


def format_summary(total, count):
    return f"Total: ${total:.2f} across {count} records"


if __name__ == "__main__":
    total = get_total(records)
    print(format_summary(total, len(records)))
    print(is_over_limit(total))
