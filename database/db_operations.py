import sqlite3
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from database.db_connection import get_connection


CENT = Decimal("0.01")


def validate_money(amount):
    """Convert an amount into a valid Decimal value."""

    try:
        amount = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid money amount.")

    if not amount.is_finite():
        raise ValueError("Money amount must be finite.")

    amount = amount.quantize(CENT, rounding=ROUND_HALF_UP)

    if amount < 0:
        raise ValueError("Money amount cannot be negative.")

    return amount


def create_user(full_name, username, pin_hash, account_number):
    """Register a new user in the database."""

    if not all([full_name, username, pin_hash, account_number]):
        raise ValueError("All user fields are required.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (
                full_name,
                username,
                pin_hash,
                account_number,
                balance
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (full_name, username, pin_hash, account_number, "0.00")
        )

        connection.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        connection.rollback()
        raise ValueError("Username or account number already exists.")

    finally:
        connection.close()


def get_user_by_username(username):
    """Find a user using their username."""

    connection = get_connection()

    try:
        return connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    finally:
        connection.close()


def get_user_by_account_number(account_number):
    """Find a user using their account number."""

    connection = get_connection()

    try:
        return connection.execute(
            "SELECT * FROM users WHERE account_number = ?",
            (account_number,)
        ).fetchone()

    finally:
        connection.close()


def get_user_by_id(user_id):
    """Find a user using their user ID."""

    connection = get_connection()

    try:
        return connection.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

    finally:
        connection.close()


def update_balance(user_id, amount):
    """Update a user's balance using a Decimal amount."""

    amount = validate_money(amount)

    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        user = connection.execute(
            "SELECT balance FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if user is None:
            raise ValueError("User account not found.")

        current_balance = Decimal(user["balance"])
        new_balance = current_balance + amount

        connection.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (str(new_balance), user_id)
        )

        connection.commit()
        return new_balance

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()