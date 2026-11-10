from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


# Location of the encryption key
KEY_PATH = Path(__file__).resolve().parent / "fernet.key"


def load_or_create_key():
    """Load the existing encryption key or create one."""

    if KEY_PATH.exists():
        key = KEY_PATH.read_bytes()
    else:
        key = Fernet.generate_key()

        try:
            with KEY_PATH.open("xb") as key_file:
                key_file.write(key)
        except FileExistsError:
            # Another process may have created the key first.
            key = KEY_PATH.read_bytes()

    # Validate the key
    Fernet(key)

    return key


def encrypt_data(data: str) -> str:
    """Encrypt text and return the encrypted value."""

    if not isinstance(data, str):
        raise TypeError("Data must be a string.")

    if not data:
        raise ValueError("Data cannot be empty.")

    key = load_or_create_key()
    fernet = Fernet(key)

    encrypted = fernet.encrypt(data.encode("utf-8"))

    return encrypted.decode("utf-8")


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt previously encrypted text."""

    if not isinstance(encrypted_data, str) or not encrypted_data:
        raise ValueError("Encrypted data cannot be empty.")

    key = load_or_create_key()
    fernet = Fernet(key)

    try:
        decrypted = fernet.decrypt(encrypted_data.encode("utf-8"))
        return decrypted.decode("utf-8")

    except (InvalidToken, UnicodeDecodeError):
        raise ValueError("Unable to decrypt the data.")