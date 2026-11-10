
import pytest

from authentication.register import (
    validate_registration,
    generate_account_number,
    register_user,
)
from authentication.login import login_user
from database import db_connection
from database.db_setup import create_tables


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Create an isolated temporary database."""

    database_path = tmp_path / "test_authentication.db"

    monkeypatch.setattr(
        db_connection,
        "DATABASE_PATH",
        database_path
    )

    create_tables()

    return database_path


def test_valid_registration_details():
    """Check valid registration information."""

    validate_registration(
        "Test User",
        "testuser",
        "123456",
        "123456"
    )


def test_invalid_username():
    """Check that a short username is rejected."""

    with pytest.raises(ValueError):
        validate_registration(
            "Test User",
            "abc",
            "123456",
            "123456"
        )


def test_invalid_pin():
    """Check that an invalid PIN is rejected."""

    with pytest.raises(ValueError):
        validate_registration(
            "Test User",
            "testuser",
            "12345",
            "12345"
        )


def test_pin_confirmation_mismatch():
    """Check that mismatched PINs are rejected."""

    with pytest.raises(ValueError):
        validate_registration(
            "Test User",
            "testuser",
            "123456",
            "654321"
        )


def test_generate_account_number():
    """Check that account numbers contain 12 digits."""

    account_number = generate_account_number()

    assert isinstance(account_number, str)
    assert len(account_number) == 12
    assert account_number.isdigit()


def test_register_user(test_database):
    """Check that a new user can register."""

    result = register_user(
        "Test User",
        "testuser",
        "123456",
        "123456"
    )

    assert result is not None


def test_login_with_correct_pin(test_database):
    """Check login using the correct PIN."""

    register_user(
        "Test User",
        "testuser",
        "123456",
        "123456"
    )

    result = login_user("testuser", "123456")

    assert result is not None



def test_login_with_wrong_pin(test_database):
    """Check that an incorrect PIN is rejected."""

    register_user(
        "Test User",
        "testuser",
        "123456",
        "123456"
    )

    with pytest.raises(ValueError, match="Invalid username or PIN"):
        login_user("testuser", "999999")
