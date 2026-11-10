
from database.db_connection import get_connection


def get_all_users():
    """Return all registered users without exposing PIN hashes."""

    connection = get_connection()

    try:
        users = connection.execute("""
            SELECT
                user_id,
                full_name,
                username,
                account_number,
                balance,
                created_at,
                is_active
            FROM users
            ORDER BY user_id DESC
        """).fetchall()

        return users

    finally:
        connection.close()


def search_user(search_value):
    """Search for a user by username or account number."""

    if not isinstance(search_value, str) or not search_value.strip():
        raise ValueError("A username or account number is required.")

    search_value = search_value.strip()

    connection = get_connection()

    try:
        user = connection.execute("""
            SELECT
                user_id,
                full_name,
                username,
                account_number,
                balance,
                created_at,
                is_active
            FROM users
            WHERE username = ? OR account_number = ?
        """, (search_value, search_value)).fetchone()

        return user

    finally:
        connection.close()


def update_user_status(user_id, is_active):
    """Activate or deactivate a user account."""

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("A valid user ID is required.")

    if not isinstance(is_active, bool):
        raise ValueError("Account status must be True or False.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE users
            SET is_active = ?
            WHERE user_id = ?
            """,
            (int(is_active), user_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("User account not found.")

        connection.commit()

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_user_count():
    """Return the total number of registered users."""

    connection = get_connection()

    try:
        result = connection.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()

        return result[0]

    finally:
        connection.close()
