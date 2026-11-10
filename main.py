
import gi
from decimal import Decimal

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

# Database
from database.db_setup import create_tables
from database.db_operations import (
    get_user_by_id,
    get_user_by_account_number,
)

# Authentication
from authentication.register import register_user
from authentication.login import login_user

# ATM operations
from atm_operations.deposit import deposit_money
from atm_operations.withdrawal import withdraw_money
from atm_operations.transfer import transfer_money

# Security
from security.session_manager import session_manager

# Transactions
from transactions.transaction_history import (
    create_transaction_table,
    record_transaction,
)

# GUI screens
from gui.screens.welcome_screen import WelcomeScreen
from gui.screens.login_screen import LoginScreen
from gui.screens.register_screen import RegisterScreen
from gui.screens.dashboard_screen import DashboardScreen
from gui.screens.deposit_screen import DepositScreen
from gui.screens.withdrawal_screen import WithdrawalScreen
from gui.screens.transfer_screen import TransferScreen
from gui.screens.history_screen import HistoryScreen

# Theme and logging
from gui.styles.theme import apply_theme
from utils.logger import log_info, log_error


class SynapseCashApp(Gtk.Application):
    """Main GTK application for SynapseCash."""

    def __init__(self):
        super().__init__(
            application_id="com.synapsecash.desktop"
        )

        self.window = None
        self.stack = None
        self.current_user = None

    def do_activate(self):
        """Initialize and display the application."""

        if self.window is not None:
            self.window.present()
            return

        try:
            # Initialize database tables
            create_tables()
            create_transaction_table()

            # Apply application theme
            apply_theme()

            # Create application window
            self.window = Gtk.ApplicationWindow(
                application=self
            )

            self.window.set_title(
                "SynapseCash - ATM Simulator"
            )

            self.window.set_default_size(1100, 750)
            self.window.set_resizable(True)

            # Create screen navigation stack
            self.stack = Gtk.Stack()

            self.stack.set_transition_type(
                Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
            )

            self.stack.set_transition_duration(250)

            self.window.set_child(self.stack)

            # Display welcome screen
            self.show_welcome()

            self.window.present()

            log_info(
                "SynapseCash application started successfully."
            )

        except Exception as error:
            log_error(
                f"Application startup failed: {error}"
            )
            raise

    def show_screen(self, screen, name):
        """Replace the current screen with another screen."""

        current_screen = self.stack.get_visible_child()

        if current_screen is not None:
            self.stack.remove(current_screen)

        self.stack.add_named(screen, name)
        self.stack.set_visible_child_name(name)

    # --------------------------------------------------
    # Welcome and authentication
    # --------------------------------------------------

    def show_welcome(self):
        """Display the welcome screen."""

        self.current_user = None

        screen = WelcomeScreen(
            on_login=self.show_login,
            on_register=self.show_register
        )

        self.show_screen(screen, "welcome")

    def show_login(self, button=None):
        """Display the login screen."""

        screen = LoginScreen(
            on_login=self.handle_login,
            on_back=lambda button: self.show_welcome()
        )

        self.show_screen(screen, "login")

    def show_register(self, button=None):
        """Display the registration screen."""

        screen = RegisterScreen(
            on_register=self.handle_registration,
            on_back=lambda button: self.show_welcome()
        )

        self.show_screen(screen, "register")

    def handle_registration(
        self,
        full_name,
        username,
        pin,
        confirm_pin
    ):
        """Register a new user."""

        try:
            user = register_user(
                full_name,
                username,
                pin,
                confirm_pin
            )

            log_info(
                f"New account registered: {user['username']}"
            )

            # Return to login after successful registration
            self.show_login()

            login_screen = self.stack.get_visible_child()

            login_screen.status_label.remove_css_class(
                "danger"
            )
            login_screen.status_label.add_css_class(
                "success"
            )

            login_screen.status_label.set_text(
                "Account created successfully! "
                f"Your account number is {user['account_number']}"
            )

        except (ValueError, RuntimeError) as error:
            screen = self.stack.get_visible_child()
            screen.show_error(str(error))

            log_error(
                f"Registration failed: {error}"
            )

        except Exception as error:
            screen = self.stack.get_visible_child()
            screen.show_error(
                "Registration could not be completed."
            )

            log_error(
                f"Unexpected registration error: {error}"
            )

    def handle_login(self, username, pin):
        """Authenticate a user and open the dashboard."""

        try:
            user = login_user(username, pin)

            self.current_user = user

            log_info(
                f"User logged in: {user['username']}"
            )

            self.show_dashboard()

        except ValueError as error:
            screen = self.stack.get_visible_child()
            screen.status_label.set_text(str(error))

            log_error(
                f"Login failed for {username}: {error}"
            )

        except Exception as error:
            screen = self.stack.get_visible_child()
            screen.status_label.set_text(
                "Unable to complete login."
            )

            log_error(
                f"Unexpected login error: {error}"
            )

    # --------------------------------------------------
    # Session management
    # --------------------------------------------------

    def check_session(self):
        """Check and refresh the active user session."""

        session = session_manager.get_session()

        if session is None:
            self.current_user = None
            self.show_welcome()
            return False

        if not session_manager.update_activity():
            self.current_user = None
            self.show_welcome()
            return False

        return True

    def handle_logout(self, button=None):
        """Log out the current user."""

        session_manager.logout()
        self.current_user = None

        log_info("User logged out.")

        self.show_welcome()

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    def show_dashboard(self, message=None):
        """Display the dashboard with updated account details."""

        if not self.check_session():
            return

        user = get_user_by_id(
            self.current_user["user_id"]
        )

        if user is None:
            self.handle_logout()
            return

        self.current_user = {
            "user_id": user["user_id"],
            "full_name": user["full_name"],
            "username": user["username"],
            "account_number": user["account_number"],
            "balance": user["balance"],
        }

        screen = DashboardScreen(
            user=self.current_user,
            on_deposit=self.show_deposit,
            on_withdrawal=self.show_withdrawal,
            on_transfer=self.show_transfer,
            on_history=self.show_history,
            on_logout=self.handle_logout
        )

        if message:
            status = Gtk.Label(label=message)
            status.add_css_class("success")
            status.set_wrap(True)
            screen.append(status)

        self.show_screen(screen, "dashboard")

    # --------------------------------------------------
    # Deposit
    # --------------------------------------------------

    def show_deposit(self, button=None):
        """Display the deposit screen."""

        if not self.check_session():
            return

        screen = DepositScreen(
            on_deposit=self.handle_deposit,
            on_back=lambda button: self.show_dashboard()
        )

        self.show_screen(screen, "deposit")

    def handle_deposit(self, amount):
        """Process a deposit and record the transaction."""

        if not self.check_session():
            return

        try:
            amount = Decimal(str(amount))

            new_balance = deposit_money(
                self.current_user["user_id"],
                amount
            )

            history_saved = self.save_transaction(
                user_id=self.current_user["user_id"],
                transaction_type="DEPOSIT",
                amount=amount,
                balance_after=new_balance,
                description="Cash deposit"
            )

            message = "Deposit successful!"

            if not history_saved:
                message += " Transaction history could not be saved."

            log_info(
                f"Deposit completed for user "
                f"{self.current_user['user_id']}"
            )

            self.show_dashboard(message)

        except (ValueError, ArithmeticError) as error:
            screen = self.stack.get_visible_child()
            screen.show_error(str(error))

            log_error(f"Deposit failed: {error}")

        except Exception as error:
            screen = self.stack.get_visible_child()
            screen.show_error(
                "Unable to complete the deposit."
            )

            log_error(
                f"Unexpected deposit error: {error}"
            )

    # --------------------------------------------------
    # Withdrawal
    # --------------------------------------------------

    def show_withdrawal(self, button=None):
        """Display the withdrawal screen."""

        if not self.check_session():
            return

        screen = WithdrawalScreen(
            on_withdraw=self.handle_withdrawal,
            on_back=lambda button: self.show_dashboard()
        )

        self.show_screen(screen, "withdrawal")

    def handle_withdrawal(self, amount):
        """Process a withdrawal and record the transaction."""

        if not self.check_session():
            return

        try:
            amount = Decimal(str(amount))

            new_balance = withdraw_money(
                self.current_user["user_id"],
                amount
            )

            history_saved = self.save_transaction(
                user_id=self.current_user["user_id"],
                transaction_type="WITHDRAWAL",
                amount=amount,
                balance_after=new_balance,
                description="Cash withdrawal"
            )

            message = "Withdrawal successful!"

            if not history_saved:
                message += " Transaction history could not be saved."

            log_info(
                f"Withdrawal completed for user "
                f"{self.current_user['user_id']}"
            )

            self.show_dashboard(message)

        except (ValueError, ArithmeticError) as error:
            screen = self.stack.get_visible_child()
            screen.show_error(str(error))

            log_error(f"Withdrawal failed: {error}")

        except Exception as error:
            screen = self.stack.get_visible_child()
            screen.show_error(
                "Unable to complete the withdrawal."
            )

            log_error(
                f"Unexpected withdrawal error: {error}"
            )

    # --------------------------------------------------
    # Money transfer
    # --------------------------------------------------

    def show_transfer(self, button=None):
        """Display the transfer screen."""

        if not self.check_session():
            return

        screen = TransferScreen(
            on_transfer=self.handle_transfer,
            on_back=lambda button: self.show_dashboard()
        )

        self.show_screen(screen, "transfer")

    def handle_transfer(self, account_number, amount):
        """Transfer money and record both transaction entries."""

        if not self.check_session():
            return

        try:
            amount = Decimal(str(amount))

            sender_id = self.current_user["user_id"]

            recipient = get_user_by_account_number(
                account_number
            )

            if recipient is None:
                raise ValueError(
                    "Recipient account was not found."
                )

            result = transfer_money(
                sender_id,
                account_number,
                amount
            )

            sent_saved = self.save_transaction(
                user_id=sender_id,
                transaction_type="TRANSFER_SENT",
                amount=amount,
                balance_after=result["sender_balance"],
                related_account=account_number,
                description="Money transferred"
            )

            received_saved = self.save_transaction(
                user_id=recipient["user_id"],
                transaction_type="TRANSFER_RECEIVED",
                amount=amount,
                balance_after=result["recipient_balance"],
                related_account=self.current_user["account_number"],
                description="Money received"
            )

            message = "Transfer successful!"

            if not sent_saved or not received_saved:
                message += " Transaction history could not be fully saved."

            log_info(
                f"Transfer completed from "
                f"{sender_id} to {recipient['user_id']}"
            )

            self.show_dashboard(message)

        except (ValueError, ArithmeticError) as error:
            screen = self.stack.get_visible_child()
            screen.show_error(str(error))

            log_error(f"Transfer failed: {error}")

        except Exception as error:
            screen = self.stack.get_visible_child()
            screen.show_error(
                "Unable to complete the transfer."
            )

            log_error(
                f"Unexpected transfer error: {error}"
            )

    # --------------------------------------------------
    # Transaction history
    # --------------------------------------------------

    def show_history(self, button=None):
        """Display the transaction history screen."""

        if not self.check_session():
            return

        screen = HistoryScreen(
            user_id=self.current_user["user_id"],
            on_back=lambda button: self.show_dashboard()
        )

        self.show_screen(screen, "history")

    # --------------------------------------------------
    # Transaction recording
    # --------------------------------------------------

    def save_transaction(
        self,
        user_id,
        transaction_type,
        amount,
        balance_after,
        related_account=None,
        description=None
    ):
        """Save a completed transaction to the history database."""

        try:
            record_transaction(
                user_id=user_id,
                transaction_type=transaction_type,
                amount=amount,
                balance_after=balance_after,
                related_account=related_account,
                description=description
            )

            return True

        except Exception as error:
            log_error(
                f"Transaction history recording failed: {error}"
            )

            return False


def main():
    """Start the SynapseCash application."""

    app = SynapseCashApp()
    app.run()


if __name__ == "__main__":
    main()
