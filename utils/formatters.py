
from datetime import datetime
from decimal import Decimal, InvalidOperation


def format_money(amount, currency="BDT"):
    """Format a monetary amount with two decimal places."""

    try:
        amount = Decimal(str(amount))

        if not amount.is_finite():
            raise InvalidOperation

        amount = amount.quantize(Decimal("0.01"))

    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Invalid monetary amount.")

    return f"{currency} {amount:,.2f}"


def format_date(date_value):
    """Format a date or datetime value for display."""

    if isinstance(date_value, datetime):
        date_object = date_value

    elif isinstance(date_value, str):
        try:
            date_object = datetime.fromisoformat(date_value)
        except ValueError:
            raise ValueError("Invalid date format.")

    else:
        raise TypeError("Date must be a string or datetime object.")

    return date_object.strftime("%d-%m-%Y")


def format_datetime(date_value):
    """Format a date and time for display."""

    if isinstance(date_value, datetime):
        date_object = date_value

    elif isinstance(date_value, str):
        try:
            date_object = datetime.fromisoformat(date_value)
        except ValueError:
            raise ValueError("Invalid date and time format.")

    else:
        raise TypeError("Value must be a string or datetime object.")

    return date_object.strftime("%d-%m-%Y %I:%M:%S %p")


def format_account_number(account_number):
    """Display a 12-digit account number in readable groups."""

    if (
        not isinstance(account_number, str)
        or len(account_number) != 12
        or not account_number.isdigit()
    ):
        raise ValueError("Invalid account number.")

    return (
        f"{account_number[:4]}-"
        f"{account_number[4:8]}-"
        f"{account_number[8:]}"
    )


def format_transaction_type(transaction_type):
    """Convert transaction codes into readable labels."""

    labels = {
        "DEPOSIT": "Cash Deposit",
        "WITHDRAWAL": "Cash Withdrawal",
        "TRANSFER_SENT": "Money Sent",
        "TRANSFER_RECEIVED": "Money Received"
    }

    if not isinstance(transaction_type, str):
        raise ValueError("Invalid transaction type.")

    transaction_type = transaction_type.upper()

    if transaction_type not in labels:
        raise ValueError("Unknown transaction type.")

    return labels[transaction_type]
