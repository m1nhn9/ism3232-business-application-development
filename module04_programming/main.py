# module04_programming/main.py
# Author: Minh Nguyen

from module04_programming.business_rules import (
    apply_discount,
    calculate_total,
    get_approval_tier,
    requires_review,
)

if __name__ == "__main__":
    price, qty = 450.00, 3
    total = calculate_total(price, qty)

    print(f"Total:          ${total:.2f}")
    print(f"Requires review: {requires_review(total)}")
    print(f"Approval tier:   {get_approval_tier(total)}")
    print(f"10% discount:    ${apply_discount(price, 10):.2f}")
