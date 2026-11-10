
from decimal import Decimal

from database.db_operations import validate_money, get_connection


def withdraw_money(user_id, amount):
    """Withdraw money safely from a user's account."""

    if not user_id:
        raise ValueError("User ID is required.")

    amount = validate_money(amount)

    if amount <= Decimal("0.00"):
        raise ValueError("Withdrawal amount must be greater than zero.")

    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        user = connection.execute(
            """
            SELECT balance, is_active
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        if user is None:
            raise ValueError("User account not found.")

        if not user["is_active"]:
            raise ValueError("This account is inactive.")

        current_balance = Decimal(user["balance"])

        if amount > current_balance:
            raise ValueError("Insufficient account balance.")

        new_balance = current_balance - amount

        connection.execute(
            """
            UPDATE users
            SET balance = ?
            WHERE user_id = ?
            """,
            (str(new_balance), user_id)
        )

        connection.commit()

        return new_balance

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
