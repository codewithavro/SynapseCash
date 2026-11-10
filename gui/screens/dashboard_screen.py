
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gui.components.custom_button import CustomButton

from gui.components.summary_card import SummaryCard


class DashboardScreen(Gtk.Box):
    """Main dashboard screen for SynapseCash."""

    def __init__(
        self,

        user,

        on_deposit=None,

        on_withdrawal=None,

        on_transfer=None,

        on_history=None,

        on_logout=None
    ):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,

            spacing=18
        )

        self.user = user

        # Main layout
        self.set_margin_top(25)

        self.set_margin_bottom(25)

        self.set_margin_start(30)

        self.set_margin_end(30)

        # Header
        header = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,

            spacing=10
        )

        title = Gtk.Label(label="SynapseCash Dashboard")

        title.add_css_class("title-1")

        title.set_hexpand(True)

        title.set_halign(Gtk.Align.START)

        logout_button = Gtk.Button(label="Logout")

        if on_logout is not None:

            logout_button.connect("clicked", on_logout)

        header.append(title)

        header.append(logout_button)

        # Welcome message

        full_name = user["full_name"]

        welcome = Gtk.Label(

            label=f"Welcome, {full_name}!"
        )

        welcome.add_css_class("heading")

        welcome.set_halign(Gtk.Align.START)

        subtitle = Gtk.Label(

            label="Here is your account overview."
        )

        subtitle.add_css_class("dim-label")

        subtitle.set_halign(Gtk.Align.START)

        # Account information
        account_label = Gtk.Label(

            label=f"Account Number: {user['account_number']}"
        )
        account_label.set_halign(Gtk.Align.START)

        # Balance card
        balance = user["balance"]

        balance_card = SummaryCard(

            "Available Balance",

            f"{balance}",

            "Your current account balance"
        )

        # Navigation buttons
        actions_title = Gtk.Label(label="Account Services")

        actions_title.add_css_class("heading")

        actions_title.set_halign(Gtk.Align.START)


        self.append(header)

        self.append(welcome)

        self.append(subtitle)

        self.append(account_label)

        self.append(balance_card)

        self.append(actions_title)

        self.add_action("Deposit Money", on_deposit)

        self.add_action("Withdraw Money", on_withdrawal)

        self.add_action("Transfer Money", on_transfer)

        self.add_action("Transaction History", on_history)

    def add_action(self, label, callback):
        
        """Add an account service button."""

        button = CustomButton(label)

        button.set_size_request(280, 45)


        if callback is not None:
            button.connect("clicked", callback)

        self.append(button)
