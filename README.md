# SynapseCash

### A Secure Desktop ATM Simulator

SynapseCash is a Python-based desktop ATM simulator designed to demonstrate basic ATM operations, secure user authentication, database management, and financial transaction handling.

The application uses GTK 4 to provide a graphical user interface and SQLite to store account information and transaction records.

---

## 1. Project Overview

**Project Name:** SynapseCash

**Project Type:** Desktop Application

**Programming Language:** Python 3.13

**GUI Framework:** GTK 4 (PyGObject)

**Database:** SQLite

**IDE:** Visual Studio Code

**Operating System:** Windows 11 (64-bit)


## 2. Main Objectives

- Develop a desktop ATM simulation application.

- Provide secure user registration and login.

- Simulate common ATM operations.

- Maintain account balances and transaction history.

- Protect sensitive information using security techniques.

## 3. Planned Features

### User Authentication

- User registration and login.

- PIN-based authentication.

- Secure PIN hashing using Argon2.

- Account lockout after repeated failed login attempts.

### ATM Operations

- Check account balance.

- Deposit money.

- Withdraw money.

- Transfer money between accounts.

- View transaction history.

### Security

- Argon2 PIN hashing.

- Fernet encryption for recoverable sensitive data.

- Account lockout mechanism.

- Session management and automatic expiration.

### Graphical User Interface

- Welcome screen.

- Login and registration screens.

- User dashboard.

- Deposit and withdrawal screens.

- Money transfer screen.

- Transaction history screen.

### Administration

- Administrator login.

- Account management.

- Basic administrative operations.

## 4. Technologies and Libraries

| Technology   | Purpose                     |
| ------------ | --------------------------- |
| Python 3.13  | Main programming language
   |
| GTK 4        | Desktop graphical interface
 |
| PyGObject    | Python integration with GTK 
|
| SQLite       | Database management      
   |
| Argon2       | Secure PIN hashing      
    |
| Cryptography | Data encryption          
   |
| Pytest       | Automated testing       
    |
| Pytest-cov   | Test coverage           
    |
| Ruff         | Code quality and linting    |

## 5. Installation and Setup

### Requirements

- Windows 11 (64-bit).

- Miniforge or Conda.

- Visual Studio Code.

- Python 3.13.

### Step 1: Clone or download the project

Open the project folder:

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

```cmd
python -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk; print(Gtkget_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version())"
```

## 6. Running the Application

The application entry point will be:

```cmd
python main.py
```

*Application startup and complete GUI integration are still under development.*

## 7. Testing

SynapseCash uses Pytest for automated testing.

Run the test suite with:

```cmd
python -m pytest tests -v
```

Generate a test coverage report with:

```cmd
python -m pytest tests --cov=. --cov-report=term-missing
```

## 8. Security Considerations

- PINs must never be stored as plaintext.

- Argon2 is used for PIN hashing.

- Sensitive recoverable information can be encrypted using Fernet.

- Encryption keys must be protected and excluded from version control.

- Database queries must use parameterized SQL.

- Financial calculations should use Python's `Decimal` type.

- Account lockout information should be stored persistently.

- Login sessions should expire after inactivity.

**Disclaimer:** SynapseCash is an educational ATM simulation project. It is not connected to real banks or financial networks and is not intended for real financial transactions.

## 10. Development Status

| Component                    | Status                                 |
| ---------------------------- | -------------------------------------- |
| Project structure            | Completed
                              |
| Python environment           | Completed       
                       |
| GTK 4 configuration          | Completed   
                           |
| Database connection          | Implemented and tested        
         |
| Database setup               | Implemented and tested         
        |
| Database operations          | Implemented and tested         
        |
| PIN hashing                  | Implemented and tested        
         |
| Data encryption              | Implemented and tested       
          |
| Account lockout              | Initial version implemented and tested
 |
| Session management           | Initial version implemented and tested
 |
| User authentication          | Pending                          
      |
| ATM operations               | Pending                   
             |
| GTK interface                | Pending                     
           |
| Admin functionality          | Pending                    
            |
| Complete application testing | Pending                                |

---

## 10. Future Improvements

- Improve persistent account security.

- Complete all ATM operations.

- Integrate all screens with GTK 4.

- Add transaction receipts.

- Add sound effects and visual notifications.

- Improve application performance and testing.

---

**Project:** SynapseCash

**Purpose:** Educational Desktop ATM Simulation

**Version:** 1.0 (Development)
