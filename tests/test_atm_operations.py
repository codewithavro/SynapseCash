
import pytest

from database import db_connection
from database.db_setup import create_tables
from database.db_operations import create_user

from atm_operations.balance import get_balance
from atm_operations.deposit import deposit_money
from atm_operations.withdrawal import withdraw_money
from atm_operations.transfer import transfer_money


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Create an isolated temporary database."""

    database_path = tmp_path / "test_atm_operations.db"

    monkeypatch.setattr(
        db_connection,
        "DATABASE_PATH",
        database_path
    )

    create_tables()

    return database_path


@pytest.fixture
def test_user(test_database):
    """Create a test user with an initial zero balance."""

    return create_user(
        "Test User",
        "testuser",
        "sample_pin_hash",
        "123456789012"
    )


def test_get_balance(test_user):
    """Check the initial account balance."""

    balance = get_balance(test_user)

    assert str(balance) == "0.00"


def test_deposit_money(test_user):
    """Check that money can be deposited."""

    new_balance = deposit_money(test_user, "500.00")

    assert str(new_balance) == "500.00"


def test_withdraw_money(test_user):
    """Check that money can be withdrawn."""

    deposit_money(test_user, "1000.00")

    new_balance = withdraw_money(test_user, "300.00")

    assert str(new_balance) == "700.00"


def test_withdraw_insufficient_balance(test_user):
    """Check that withdrawal is rejected when funds are insufficient."""

    with pytest.raises(ValueError):
        withdraw_money(test_user, "500.00")


def test_transfer_money(test_database):
    """Check that money can be transferred between accounts."""

    sender_id = create_user(
        "Sender User",
        "sender",
        "sample_pin_hash",
        "111111111111"
    )

    recipient_id = create_user(
        "Recipient User",
        "recipient",
        "sample_pin_hash",
        "222222222222"
    )

    deposit_money(sender_id, "1000.00")

    result = transfer_money(
        sender_id,
        "222222222222",
        "300.00"
    )

    assert str(result["sender_balance"]) == "700.00"
    assert str(result["recipient_balance"]) == "300.00"

    assert str(get_balance(recipient_id)) == "300.00"
