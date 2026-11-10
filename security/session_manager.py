from datetime import datetime, timedelta, timezone
from threading import Lock


# Session security settings
SESSION_TIMEOUT_MINUTES = 10


class SessionManager:
    """Manage user login sessions."""

    def __init__(self):
        self._session = None
        self._lock = Lock()

    def create_session(self, user_id, account_number):
        """Create a new session after successful login."""

        if not user_id or not account_number:
            raise ValueError("User ID and account number are required.")

        with self._lock:
            self._session = {
                "user_id": user_id,
                "account_number": account_number,
                "created_at": datetime.now(timezone.utc),
                "last_activity": datetime.now(timezone.utc)
            }

    def get_session(self):
        """Return the current session if it is still valid."""

        with self._lock:
            if self._session is None:
                return None

            now = datetime.now(timezone.utc)
            last_activity = self._session["last_activity"]

            if now - last_activity >= timedelta(
                minutes=SESSION_TIMEOUT_MINUTES
            ):
                self._session = None
                return None

            return self._session.copy()

    def update_activity(self):
        """Refresh the session activity time."""

        with self._lock:
            if self._session is None:
                return False

            now = datetime.now(timezone.utc)

            if now - self._session["last_activity"] >= timedelta(
                minutes=SESSION_TIMEOUT_MINUTES
            ):
                self._session = None
                return False

            self._session["last_activity"] = now
            return True

    def is_logged_in(self):
        """Check whether a valid session exists."""

        return self.get_session() is not None

    def logout(self):
        """End the current session."""

        with self._lock:
            self._session = None


# Shared session manager for the application
session_manager = SessionManager()