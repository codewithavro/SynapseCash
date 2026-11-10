from datetime import datetime, timedelta, timezone
from threading import Lock


# Account security settings
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_DURATION_MINUTES = 5


# Temporary storage for failed login attempts
_failed_attempts = {}
_locked_accounts = {}

# Protect shared data from simultaneous access
_security_lock = Lock()


def record_failed_attempt(account_number: str) -> bool:
    """Record a failed login attempt.

    Returns True if the account becomes locked.
    """

    if not account_number:
        raise ValueError("Account number is required.")

    with _security_lock:
        now = datetime.now(timezone.utc)

        lock_until = _locked_accounts.get(account_number)

        if lock_until and now < lock_until:
            return True

        if lock_until and now >= lock_until:
            _locked_accounts.pop(account_number, None)
            _failed_attempts.pop(account_number, None)

        attempts = _failed_attempts.get(account_number, 0) + 1
        _failed_attempts[account_number] = attempts

        if attempts >= MAX_FAILED_ATTEMPTS:
            _locked_accounts[account_number] = (
                now + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            )
            return True

        return False


def is_account_locked(account_number: str) -> bool:
    """Check whether an account is currently locked."""

    with _security_lock:
        lock_until = _locked_accounts.get(account_number)

        if lock_until is None:
            return False

        if datetime.now(timezone.utc) >= lock_until:
            _locked_accounts.pop(account_number, None)
            _failed_attempts.pop(account_number, None)
            return False

        return True


def reset_failed_attempts(account_number: str) -> None:
    """Reset failed attempts after successful login."""

    with _security_lock:
        _failed_attempts.pop(account_number, None)
        _locked_accounts.pop(account_number, None)


def get_remaining_attempts(account_number: str) -> int:
    """Return the number of login attempts remaining."""

    with _security_lock:
        lock_until = _locked_accounts.get(account_number)

        if lock_until and datetime.now(timezone.utc) < lock_until:
            return 0

        if lock_until:
            _locked_accounts.pop(account_number, None)
            _failed_attempts.pop(account_number, None)

        attempts = _failed_attempts.get(account_number, 0)

        return max(0, MAX_FAILED_ATTEMPTS - attempts)