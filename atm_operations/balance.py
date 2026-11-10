
from decimal import Decimal, InvalidOperation

from database.db_operations import get_user_by_id


def get_balance(user_id):
    """Retrieve and return a user's account balance."""

    if not user_id:
        raise ValueError("User ID is required.")

    user = get_user_by_id(user_id)

    if user is None:
        raise ValueError("User account not found.")

    if not user["is_active"]:
        raise ValueError("This account is inactive.")

    try:
        balance = Decimal(user["balance"])
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Invalid account balance.")

    if not balance.is_finite() or balance < 0:
        raise ValueError("Account balance is invalid.")

    return balance
