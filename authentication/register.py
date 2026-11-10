
import secrets
import string

from database.db_operations import (
    create_user,
    get_user_by_username,
)
from security.password_hashing import hash_pin


def validate_registration(full_name, username, pin, confirm_pin):
    """Validate user registration information."""

    if not all([full_name, username, pin, confirm_pin]):
        raise ValueError("All fields are required.")

    full_name = full_name.strip()
    username = username.strip()

    if not full_name:
        raise ValueError("Full name cannot be empty.")

    if not username:
        raise ValueError("Username cannot be empty.")

    if len(full_name) > 100:
        raise ValueError("Full name is too long.")

    if len(username) < 4 or len(username) > 30:
        raise ValueError("Username must contain 4–30 characters.")

    if not all(
        character.isalnum() or character == "_"
        for character in username
    ):
        raise ValueError(
            "Username can contain only letters, numbers, and underscores."
        )

    if not pin.isdigit() or len(pin) != 6:
        raise ValueError("PIN must contain exactly 6 digits.")

    if pin != confirm_pin:
        raise ValueError("PINs do not match.")

    return full_name, username


def generate_account_number():
    """Generate a 12-digit account number."""

    return "".join(secrets.choice(string.digits) for _ in range(12))


def register_user(full_name, username, pin, confirm_pin):
    """Register a new SynapseCash user."""

    full_name, username = validate_registration(
        full_name,
        username,
        pin,
        confirm_pin
    )

    if get_user_by_username(username):
        raise ValueError("Username already exists.")

    pin_hash = hash_pin(pin)

    # Retry if an account number already exists.
    for _ in range(5):
        account_number = generate_account_number()

        try:
            user_id = create_user(
                full_name,
                username,
                pin_hash,
                account_number
            )

            return {
                "user_id": user_id,
                "full_name": full_name,
                "username": username,
                "account_number": account_number
            }

        except ValueError as error:
            if "account number already exists" not in str(error).lower():
                raise

    raise RuntimeError("Could not generate a unique account number.")
