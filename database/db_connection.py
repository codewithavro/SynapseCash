import sqlite3
from pathlib import Path


# Locate the SynapseCash project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database file location
DATABASE_PATH = BASE_DIR / "database" / "synapsecash.db"


def get_connection():
    """Create and return a database connection."""

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection