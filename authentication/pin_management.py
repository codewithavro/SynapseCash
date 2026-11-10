
from database.db_connection import get_connection
from database.db_operations import get_user_by_id
from security.password_hashing import hash_pin, verify_pin


def validate_new_pin(new_pin, confirm_pin):
    """Validate a new six-digit PIN."""

    if not isinstance(new_pin, str) or not new_pin.isdigit():
        raise ValueError("PIN must contain only digits.")

    if len(new_pin) != 6:
        raise ValueError("PIN must contain exactly 6 digits.")

    if new_pin != confirm_pin:
        raise ValueError("New PINs do not match.")

    return True


def change_pin(user_id, current_pin, new_pin, confirm_pin):
    """Change a user's PIN after verifying the current PIN."""

    if not all([user_id, current_pin, new_pin, confirm_pin]):
        raise ValueError("All fields are required.")

    user = get_user_by_id(user_id)

    if user is None:
        raise ValueError("User account not found.")

    if not user["is_active"]:
        raise ValueError("This account is inactive.")

    if not verify_pin(current_pin, user["pin_hash"]):
        raise ValueError("Current PIN is incorrect.")

    validate_new_pin(new_pin, confirm_pin)

    if verify_pin(new_pin, user["pin_hash"]):
        raise ValueError("New PIN must be different from current PIN.")

    new_pin_hash = hash_pin(new_pin)

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET pin_hash = ?
            WHERE user_id = ?
            """,
            (new_pin_hash, user_id)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return True
