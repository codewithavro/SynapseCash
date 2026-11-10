from database.db_connection import get_connection


def create_tables():
    """Create the initial SynapseCash database tables."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                pin_hash TEXT NOT NULL,
                account_number TEXT NOT NULL UNIQUE,
                balance TEXT NOT NULL DEFAULT '0.00',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)

        connection.commit()
        print("Database tables created successfully!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()