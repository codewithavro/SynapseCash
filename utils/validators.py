
import re
from decimal import Decimal, InvalidOperation


def validate_required_text(value, field_name="Field"):
    """Check that a required text value is not empty."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required.")

    return value.strip()


def validate_username(username):
    """Validate a username."""

    username = validate_required_text(username, "Username")

    if not re.fullmatch(r"[A-Za-z0-9_]{4,30}", username):
        raise ValueError(
            "Username must be 4-30 characters and contain "
            "only letters, numbers, and underscores."
        )

    return username


def validate_pin(pin):
    """Validate a six-digit PIN."""

    if not isinstance(pin, str) or not re.fullmatch(r"\d{6}", pin):
        raise ValueError("PIN must contain exactly 6 digits.")

    return pin


def validate_account_number(account_number):
    """Validate a twelve-digit account number."""

    if (
        not isinstance(account_number, str)
        or not re.fullmatch(r"\d{12}", account_number)
    ):
        raise ValueError(
            "Account number must contain exactly 12 digits."
        )

    return account_number


def validate_money(amount):
    """Convert and validate a positive monetary amount."""

    try:
        amount = Decimal(str(amount))

        if not amount.is_finite():
            raise InvalidOperation

        amount = amount.quantize(Decimal("0.01"))

    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Please enter a valid money amount.")

    if amount <= Decimal("0.00"):
        raise ValueError("Amount must be greater than zero.")

    return amount
