
import pytest

from security.password_hashing import (
    hash_pin,
    verify_pin,
    needs_rehash,
)
from security import encryption
from security.encryption import encrypt_data, decrypt_data
from security.account_lock import (
    record_failed_attempt,
    is_account_locked,
    reset_failed_attempts,
    get_remaining_attempts,
)
from security.session_manager import SessionManager


def test_pin_hashing():
    """Check that a PIN is securely hashed."""

    hashed_pin = hash_pin("123456")

    assert hashed_pin != "123456"
    assert verify_pin("123456", hashed_pin)


def test_wrong_pin_verification():
    """Check that an incorrect PIN fails verification."""

    hashed_pin = hash_pin("123456")

    assert not verify_pin("999999", hashed_pin)


def test_empty_pin_rejected():
    """Check that an empty PIN cannot be hashed."""

    with pytest.raises(ValueError):
        hash_pin("")


def test_encryption_and_decryption(tmp_path, monkeypatch):
    """Check that encrypted data can be decrypted."""

    key_path = tmp_path / "test_fernet.key"

    monkeypatch.setattr(encryption, "KEY_PATH", key_path)

    original_text = "SynapseCash confidential information"

    encrypted_text = encrypt_data(original_text)

    assert encrypted_text != original_text
    assert decrypt_data(encrypted_text) == original_text


def test_account_lockout():
    """Check account lockout after three failed attempts."""

    account_number = "999999999991"

    reset_failed_attempts(account_number)

    assert not is_account_locked(account_number)

    record_failed_attempt(account_number)
    record_failed_attempt(account_number)

    assert get_remaining_attempts(account_number) == 1
    assert not is_account_locked(account_number)

    record_failed_attempt(account_number)

    assert is_account_locked(account_number)

    reset_failed_attempts(account_number)

    assert not is_account_locked(account_number)


def test_session_creation_and_logout():
    """Check that a session can be created and closed."""

    manager = SessionManager()

    manager.create_session(101, "123456789012")

    assert manager.is_logged_in()

    manager.logout()

    assert not manager.is_logged_in()


def test_session_activity():
    """Check that session activity can be updated."""

    manager = SessionManager()

    manager.create_session(102, "987654321098")

    assert manager.is_logged_in()

    manager.update_activity()

    assert manager.is_logged_in()

    manager.logout()
