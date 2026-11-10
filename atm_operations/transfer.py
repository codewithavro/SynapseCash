
from decimal import Decimal

from database.db_operations import validate_money
from database.db_connection import get_connection


def transfer_money(sender_user_id, recipient_account_number, amount):
    """Transfer money safely between two SynapseCash accounts."""

    if not sender_user_id or not recipient_account_number:
        raise ValueError("Sender and recipient information are required.")

    recipient_account_number = recipient_account_number.strip()

    if not recipient_account_number:
        raise ValueError("Recipient account number is required.")

    amount = validate_money(amount)

    if amount <= Decimal("0.00"):
        raise ValueError("Transfer amount must be greater than zero.")

    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        sender = connection.execute(
            """
            SELECT user_id, balance, is_active
            FROM users
            WHERE user_id = ?
            """,
            (sender_user_id,)
        ).fetchone()

        if sender is None:
            raise ValueError("Sender account not found.")

        if not sender["is_active"]:
            raise ValueError("Sender account is inactive.")

        recipient = connection.execute(
            """
            SELECT user_id, balance, is_active
            FROM users
            WHERE account_number = ?
            """,
            (recipient_account_number,)
        ).fetchone()

        if recipient is None:
            raise ValueError("Recipient account not found.")

        if not recipient["is_active"]:
            raise ValueError("Recipient account is inactive.")

        if sender["user_id"] == recipient["user_id"]:
            raise ValueError("Cannot transfer money to the same account.")

        sender_balance = Decimal(sender["balance"])
        recipient_balance = Decimal(recipient["balance"])

        if amount > sender_balance:
            raise ValueError("Insufficient account balance.")

        new_sender_balance = sender_balance - amount
        new_recipient_balance = recipient_balance + amount

        connection.execute(
            """
            UPDATE users
            SET balance = ?
            WHERE user_id = ?
            """,
            (str(new_sender_balance), sender["user_id"])
        )

        connection.execute(
            """
            UPDATE users
            SET balance = ?
            WHERE user_id = ?
            """,
            (str(new_recipient_balance), recipient["user_id"])
        )

        connection.commit()

        return {
            "sender_balance": new_sender_balance,
            "recipient_balance": new_recipient_balance
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
