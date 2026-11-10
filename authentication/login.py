
from database.db_operations import get_user_by_username
from security.password_hashing import verify_pin
from security.account_lock import (
    record_failed_attempt,
    is_account_locked,
    get_remaining_attempts,
    reset_failed_attempts,
)
from security.session_manager import session_manager


def login_user(username, pin):
    """Authenticate a user and create a login session."""

    if not username or not pin:
        raise ValueError("Username and PIN are required.")

    username = username.strip()

    # Find the account
    user = get_user_by_username(username)

    if user is None:
        raise ValueError("Invalid username or PIN.")

    account_number = user["account_number"]

    # Check account status
    if not user["is_active"]:
        raise ValueError("This account is inactive.")

    # Check account lockout
    if is_account_locked(account_number):
        raise ValueError(
            "Account is temporarily locked. Please try again later."
        )

    # Verify PIN
    if not verify_pin(pin, user["pin_hash"]):
        record_failed_attempt(account_number)

        if is_account_locked(account_number):
            raise ValueError(
                "Account locked after too many incorrect PIN attempts."
            )

        remaining = get_remaining_attempts(account_number)

        raise ValueError(
            f"Invalid username or PIN. "
            f"{remaining} attempt(s) remaining."
        )

    # Successful authentication
    reset_failed_attempts(account_number)

    session_manager.create_session(
        user["user_id"],
        account_number
    )

    return {
        "user_id": user["user_id"],
        "full_name": user["full_name"],
        "username": user["username"],
        "account_number": account_number,
        "balance": user["balance"],
    }
