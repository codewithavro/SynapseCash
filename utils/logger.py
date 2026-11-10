
import logging
from pathlib import Path


# Locate the SynapseCash logs folder
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

# Create the logs folder if it does not exist
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "synapsecash.log"


def get_logger(name="SynapseCash"):
    """Create and return a configured application logger."""

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


# Shared application logger
app_logger = get_logger()


def log_info(message):
    """Record an informational event."""

    app_logger.info(message)


def log_warning(message):
    """Record a warning."""

    app_logger.warning(message)


def log_error(message):
    """Record an error."""

    app_logger.error(message)


def log_exception(message):
    """Record an error with exception details."""

    app_logger.exception(message)
