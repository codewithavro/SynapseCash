
from datetime import datetime
from decimal import Decimal


def generate_receipt(
    transaction_id,
    transaction_type,
    amount,
    balance_after,
    account_number,
    related_account=None,
    description=None
):
    """Generate a formatted receipt for an ATM transaction."""

    if not transaction_id or not account_number:
        raise ValueError("Transaction ID and account number are required.")

    transaction_type = transaction_type.upper()

    valid_types = {
        "DEPOSIT",
        "WITHDRAWAL",
        "TRANSFER_SENT",
        "TRANSFER_RECEIVED",
    }

    if transaction_type not in valid_types:
        raise ValueError("Invalid transaction type.")

    try:
        amount = Decimal(str(amount))
        balance_after = Decimal(str(balance_after))
    except Exception:
        raise ValueError("Invalid transaction amount.")

    if not amount.is_finite() or not balance_after.is_finite():
        raise ValueError("Receipt amounts must be finite.")

    if amount <= Decimal("0.00") or balance_after < Decimal("0.00"):
        raise ValueError("Invalid receipt amount or balance.")

    if transaction_type in {"TRANSFER_SENT", "TRANSFER_RECEIVED"}:
        if not related_account:
            raise ValueError("Related account is required for transfers.")

    transaction_names = {
        "DEPOSIT": "Cash Deposit",
        "WITHDRAWAL": "Cash Withdrawal",
        "TRANSFER_SENT": "Money Transfer (Sent)",
        "TRANSFER_RECEIVED": "Money Transfer (Received)",
    }

    current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    receipt = [
        "================================",
        "          SYNAPSECASH",
        "       ATM TRANSACTION RECEIPT",
        "================================",
        f"Transaction ID : {transaction_id}",
        f"Date and Time  : {current_time}",
        f"Transaction    : {transaction_names[transaction_type]}",
        f"Account Number : {account_number}",
        f"Amount         : {amount:.2f}",
    ]

    if related_account:
        receipt.append(f"Related Account: {related_account}")

    if description:
        receipt.append(f"Description    : {description}")

    receipt.extend([
        "--------------------------------",
        f"Available Balance: {balance_after:.2f}",
        "================================",
        "       Thank you for using",
        "          SYNAPSECASH",
        "================================",
    ])

    return "\n".join(receipt)
