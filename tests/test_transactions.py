
import pytest

from database import db_connection
from database.db_setup import create_tables
from database.db_operations import create_user

from transactions.transaction_history import (
    record_transaction,
    get_transaction_history,
)
from transactions.receipt import generate_receipt


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Create an isolated temporary database."""

    database_path = tmp_path / "test_transactions.db"

    monkeypatch.setattr(
        db_connection,
        "DATABASE_PATH",
        database_path
    )

    create_tables()

    return database_path


@pytest.fixture
def test_user(test_database):
    """Create a test user."""

    return create_user(
        "Test User",
        "testuser",
        "sample_pin_hash",
        "123456789012"
    )


def test_record_transaction(test_user):
    """Check that a transaction can be recorded."""

    transaction_id = record_transaction(
        test_user,
        "DEPOSIT",
        "500.00",
        "500.00",
        description="Test deposit"
    )

    assert transaction_id > 0


def test_get_transaction_history(test_user):
    """Check that transaction history can be retrieved."""

    record_transaction(
        test_user,
        "DEPOSIT",
        "500.00",
        "500.00"
    )

    history = get_transaction_history(test_user)

    assert len(history) == 1
    assert history[0]["transaction_type"] == "DEPOSIT"
    assert history[0]["amount"] == "500.00"


def test_invalid_transaction_type(test_user):
    """Check that an invalid transaction type is rejected."""

    with pytest.raises(ValueError):
        record_transaction(
            test_user,
            "INVALID",
            "100.00",
            "100.00"
        )


def test_zero_transaction_amount(test_user):
    """Check that a zero transaction amount is rejected."""

    with pytest.raises(ValueError):
        record_transaction(
            test_user,
            "DEPOSIT",
            "0.00",
            "0.00"
        )


def test_generate_receipt():
    """Check that a transaction receipt can be generated."""

    receipt = generate_receipt(
        1,
        "DEPOSIT",
        "500.00",
        "500.00",
        "123456789012",
        description="Test deposit"
    )

    assert isinstance(receipt, str)
    assert len(receipt) > 0
    assert "500.00" in receipt
    assert "123456789012" in receipt
