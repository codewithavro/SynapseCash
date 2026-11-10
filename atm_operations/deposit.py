
from decimal import Decimal

from database.db_operations import validate_money, update_balance


def deposit_money(user_id, amount):
    """Deposit money into a user's account."""

    if not user_id:
        raise ValueError("User ID is required.")

    amount = validate_money(amount)

    if amount <= Decimal("0.00"):
        raise ValueError("Deposit amount must be greater than zero.")

    new_balance = update_balance(user_id, amount)

    return new_balance
