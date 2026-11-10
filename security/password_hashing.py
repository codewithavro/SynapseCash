from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)


# Create the Argon2 password hasher
_password_hasher = PasswordHasher()


def hash_pin(pin: str) -> str:
    """Securely hash a user's PIN."""

    if not isinstance(pin, str) or not pin:
        raise ValueError("PIN cannot be empty.")

    return _password_hasher.hash(pin)


def verify_pin(pin: str, pin_hash: str) -> bool:
    """Verify a PIN against its stored hash."""

    if not isinstance(pin, str) or not pin:
        return False

    if not isinstance(pin_hash, str) or not pin_hash:
        return False

    try:
        return _password_hasher.verify(pin_hash, pin)

    except (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError
    ):
        return False


def needs_rehash(pin_hash: str) -> bool:
    """Check whether a stored PIN hash needs updating."""

    try:
        return _password_hasher.check_needs_rehash(pin_hash)

    except (VerificationError, InvalidHashError):
        return True