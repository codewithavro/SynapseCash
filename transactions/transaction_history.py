
from decimal import Decimal

from database.db_connection import get_connection
from database.db_operations import validate_money


VALID_TRANSACTION_TYPES = {
    "DEPOSIT",
    "WITHDRAWAL",
    "TRANSFER_SENT",
    "TRANSFER_RECEIVED",
}


def create_transaction_table():
    """Create the transaction history table if it does not exist."""

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                amount TEXT NOT NULL,
                balance_after TEXT NOT NULL,
                related_account TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()

    finally:
        connection.close()


def record_transaction(
    user_id,
    transaction_type,
    amount,
    balance_after,
    related_account=None,
    description=None
):
    """Save a transaction in the database."""

    if not user_id:
        raise ValueError("User ID is required.")

    transaction_type = transaction_type.upper()

    if transaction_type not in VALID_TRANSACTION_TYPES:
        raise ValueError("Invalid transaction type.")

    amount = validate_money(amount)
    balance_after = validate_money(balance_after)

    if amount <= Decimal("0.00"):
        raise ValueError("Transaction amount must be greater than zero.")

    create_transaction_table()

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO transactions (
                user_id,
                transaction_type,
                amount,
                balance_after,
                related_account,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                transaction_type,
                str(amount),
                str(balance_after),
                related_account,
                description
            )
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_transaction_history(user_id, limit=50):
    """Return the most recent transactions for a user."""

    if not user_id:
        raise ValueError("User ID is required.")

    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    create_transaction_table()

    connection = get_connection()

    try:
        transactions = connection.execute(
            """
            SELECT *
            FROM transactions
            WHERE user_id = ?
            ORDER BY transaction_id DESC
            LIMIT ?
            """,
            (user_id, limit)
        ).fetchall()

        return transactions

    finally:
        connection.close()
