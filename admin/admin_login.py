
import re
import sqlite3

from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)

from database.db_connection import get_connection


_password_hasher = PasswordHasher()


def create_admin_table():
    """Create a separate table for administrator accounts."""

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)

        connection.commit()

    finally:
        connection.close()


def validate_admin_credentials(username, password):
    """Validate administrator registration details."""

    if not isinstance(username, str) or not username:
        raise ValueError("Username is required.")

    if not re.fullmatch(r"[A-Za-z0-9_]{4,30}", username):
        raise ValueError(
            "Username must be 4-30 characters and contain "
            "only letters, numbers, and underscores."
        )

    if not isinstance(password, str) or len(password) < 12:
        raise ValueError(
            "Administrator password must contain at least 12 characters."
        )


def create_admin(username, password, confirm_password):
    """Create a new administrator account."""

    validate_admin_credentials(username, password)

    if password != confirm_password:
        raise ValueError("Passwords do not match.")

    create_admin_table()

    password_hash = _password_hasher.hash(password)

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO admins (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:
        connection.rollback()
        raise ValueError("Administrator username already exists.")

    finally:
        connection.close()


def login_admin(username, password):
    """Authenticate an administrator."""

    if not isinstance(username, str) or not username:
        return None

    if not isinstance(password, str) or not password:
        return None

    create_admin_table()

    connection = get_connection()

    try:
        admin = connection.execute(
            """
            SELECT *
            FROM admins
            WHERE username = ? AND is_active = 1
            """,
            (username,)
        ).fetchone()

    finally:
        connection.close()

    if admin is None:
        return None

    try:
        if _password_hasher.verify(
            admin["password_hash"],
            password
        ):
            return {
                "admin_id": admin["admin_id"],
                "username": admin["username"],
                "created_at": admin["created_at"]
            }

    except (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError
    ):
        return None

    return None
