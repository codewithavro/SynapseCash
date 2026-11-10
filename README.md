# SynapseCash

### A Secure Desktop ATM Simulator

SynapseCash is a Python-based desktop ATM simulator designed to demonstrate user authentication, account management, financial transactions, database operations, and application security.

The project uses GTK 4 for its graphical user interface and SQLite for database management. It is developed as an educational application and does not connect to real banking networks.

---

## 1. Project Overview

| Information | Details |
|---|---|
| Project Name | SynapseCash |
| Project Type | Desktop ATM Simulator |
| Programming Language | Python 3.13 |
| GUI Framework | GTK 4 |
| Python GUI Integration | PyGObject |
| Database | SQLite |
| Security | Argon2 and Fernet |
| IDE | Visual Studio Code |
| Operating System | Windows 11 (64-bit) |

## 2. Project Objectives

- Develop a desktop ATM simulation application.
- Implement secure user registration and login.
- Simulate common ATM operations.
- Maintain account balances and transaction records.
- Protect sensitive information using security techniques.
- Provide a graphical interface using GTK 4.
- Practice Python programming, database management, and software testing.

## 3. Main Features

### User Authentication
- User registration and login.
- Six-digit PIN authentication.
- Secure PIN hashing using Argon2.
- Account lockout after repeated failed login attempts.
- PIN management.

### ATM Operations
- Check account balance.
- Deposit money.
- Withdraw money.
- Transfer money between accounts.

### Transaction Management
- Record financial transactions.
- View transaction history.
- Generate transaction receipts.
- Store transaction details in SQLite.

### Security
- Argon2 PIN hashing.
- Fernet encryption for sensitive recoverable information.
- Account lockout mechanism.
- Session management.
- Automatic session expiration.
- Parameterized SQL queries.

### Graphical User Interface
- Welcome screen.
- Login screen.
- Registration screen.
- Dashboard.
- Deposit screen.
- Withdrawal screen.
- Money transfer screen.
- Transaction history screen.
- Reusable GUI components.
- Custom GTK styling.

### Administration
- Administrator authentication.
- User account management.
- User search.
- Account status management.
- User count information.

### Additional Features
- Application logging.
- Input validation.
- Money and date formatting.
- OGG sound effects.
- Image assets.
- Automated testing.

## 4. Technologies and Libraries

| Technology | Purpose |
|---|---|
| Python 3.13 | Main programming language |
| GTK 4 | Desktop graphical interface |
| PyGObject | Python integration with GTK |
| SQLite | Database management |
| Argon2 | Secure PIN hashing |
| Cryptography | Fernet encryption |
| Pytest | Automated testing |
| Pytest-cov | Test coverage |
| Ruff | Code quality and linting |

## 5. Project Structure

```text
SynapseCash/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── admin/
│   ├── admin_login.py
│   └── admin_operations.py
│
├── assets/
│   ├── images/
│   │   ├── logo/
│   │   ├── icons/
│   │   ├── backgrounds/
│   │   └── atm_illustrations/
│   │
│   └── sounds/
│
├── authentication/
│   ├── register.py
│   ├── login.py
│   └── pin_management.py
│
├── atm_operations/
│   ├── balance.py
│   ├── deposit.py
│   ├── withdrawal.py
│   └── transfer.py
│
├── database/
│   ├── db_connection.py
│   ├── db_setup.py
│   └── db_operations.py
│
├── security/
│   ├── password_hashing.py
│   ├── encryption.py
│   ├── account_lock.py
│   └── session_manager.py
│
├── gui/
│   ├── screens/
│   ├── components/
│   └── styles/
│
├── transactions/
│   ├── transaction_history.py
│   └── receipt.py
│
├── utils/
│   ├── validators.py
│   ├── formatters.py
│   └── logger.py
│
├── tests/
│   ├── test_database.py
│   ├── test_authentication.py
│   ├── test_security.py
│   ├── test_atm_operations.py
│   └── test_transactions.py
│
└── logs/
```

## 6. Installation and Setup

### Requirements

- Windows 11 (64-bit).
- Miniforge or Conda.
- Visual Studio Code.
- Python 3.13.
- Git (optional).

### Step 1: Open the project folder

Open Command Prompt or the VS Code terminal:

```cmd
cd /d D:\SynapseCash
```

### Step 2: Activate the Conda environment

```cmd
conda activate synapsecash
```

### Step 3: Install Python dependencies

```cmd
python -m pip install -r requirements.txt
```

### Step 4: Verify GTK 4

Run:

```cmd
python -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk; print('GTK:', Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version())"
```

A successful installation should display the GTK version.

## 7. Running the Application

The planned application entry point is:

```cmd
python main.py
```

The main application integration and startup workflow are still under development.

## 8. Testing

SynapseCash uses Pytest for automated testing.

Run all tests:

```cmd
python -m pytest tests/ -v
```

Run an individual test file:

```cmd
python -m pytest tests/test_database.py -v
```

Generate a test coverage report:

```cmd
python -m pytest tests/ --cov=. --cov-report=term-missing
```

### Current Test Results

**35 automated tests passed successfully.**

| Test Module | Passed Tests |
|---|---:|
| ATM Operations | 5 |
| Authentication | 8 |
| Database | 10 |
| Security | 7 |
| Transactions | 5 |
| **Total** | **35** |

## 9. Security Considerations

- Never store PINs as plaintext.
- Use Argon2 for PIN hashing.
- Protect encryption keys and exclude them from version control.
- Use parameterized SQL queries.
- Use Python's `Decimal` type for financial calculations.
- Maintain account lockout information.
- Expire inactive login sessions.
- Validate user input before processing operations.
- Use database transactions for financial updates.

## 10. Development Status

| Component | Status |
|---|---|
| Project structure | Complete |
| Python environment | Complete |
| GTK 4 configuration | Complete |
| Database | Complete |
| Security | Complete |
| Authentication | Complete |
| ATM Operations | Complete |
| Transaction management | Complete |
| GUI screens and components | Complete |
| Admin functionality | Complete |
| Assets | Complete |
| Utility modules | Complete |
| Automated tests | Complete — 35 passed |
| Logging | Complete |
| Main application integration | Pending |

## 11. Future Improvements

- Complete GTK application integration.
- Implement screen navigation and application startup.
- Connect GUI actions to backend operations.
- Integrate transaction recording with financial operations.
- Add transaction receipt printing.
- Improve application notifications and sound effects.
- Expand automated test coverage.
- Improve overall application performance.

## 12. Disclaimer

SynapseCash is an educational desktop ATM simulation project. It is not connected to real banks, payment systems, or financial networks.

It is intended for learning and demonstration purposes only and must not be used for real financial transactions.

---

**Project:** SynapseCash  
**Version:** 1.0 (Development)  
**Platform:** Windows 11 (64-bit)  
**Purpose:** Educational Desktop ATM Simulation