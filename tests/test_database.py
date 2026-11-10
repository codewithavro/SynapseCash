
import pytest

from database import db_connection
from database.db_setup import create_tables
from database.db_operations import (
    create_user,
    get_user_by_username,
    get_user_by_account_number,
    get_user_by_id,
    update_balance,
    validate_money,
)


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Create an isolated temporary database for each test."""

    database_path = tmp_path / "test_synapsecash.db"

    monkeypatch.setattr(
        db_connection,
        "DATABASE_PATH",
        database_path
    )

    create_tables()

    return database_path


def test_create_tables(test_database):
    """Check that the users table is created."""

    connection = db_connection.get_connection()

    try:
        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'users'
        """).fetchone()

        assert result is not None

    finally:
        connection.close()


def test_create_user(test_database):
    """Check that a new user can be created."""

    user_id = create_user(
        "Test User",
        "testuser",
        "sample_pin_hash",
        "123456789012"
    )

    assert user_id > 0

    user = get_user_by_id(user_id)

    assert user["full_name"] == "Test User"
    assert user["username"] == "testuser"
    assert user["account_number"] == "123456789012"
    assert user["balance"] == "0.00"


def test_get_user_by_username(test_database):
    """Check user lookup by username."""

    create_user(
        "Test User",
        "testuser",
        "sample_pin_hash",
        "123456789012"
    )

    user = get_user_by_username("testuser")

    assert user is not None
    assert user["username"] == "testuser"


def test_get_user_by_account_number(test_database):
    """Check user lookup by account number."""

    create_user(
        "Test User",
        "testuser",
        "sample_pin_hash",
        "123456789012"
    )

    user = get_user_by_account_number("123456789012")

    assert user is not None
    assert user["account_number"] == "123456789012"


def test_update_balance(test_database):
    """Check that a user's balance can be updated."""

    user_id = create_user(
        "Test User",
        "testuser",
        "sample_pin_hash",
        "123456789012"
    )

    new_balance = update_balance(user_id, "500.00")

    assert new_balance == validate_money("500.00")

    user = get_user_by_id(user_id)

    assert user["balance"] == "500.00"


def test_duplicate_user_is_rejected(test_database):
    """Check that duplicate usernames are rejected."""

    create_user(
        "Test User",
        "testuser",
        "sample_pin_hash",
        "123456789012"
    )

    with pytest.raises(ValueError):
        create_user(
            "Another User",
            "testuser",
            "another_pin_hash",
            "987654321098"
        )


@pytest.mark.parametrize(
    "amount",
    ["invalid", "-100", "NaN", "Infinity"]
)
def test_invalid_money_is_rejected(test_database, amount):
    """Check that invalid monetary amounts are rejected."""

    with pytest.raises(ValueError):
        validate_money(amount)
