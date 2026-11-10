
import gi
from decimal import Decimal, InvalidOperation

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gui.components.custom_button import CustomButton


class TransferScreen(Gtk.Box):
    """Money transfer screen for SynapseCash."""

    def __init__(self, on_transfer=None, on_back=None):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=15
        )

        self.on_transfer = on_transfer

        # Screen layout
        self.set_halign(Gtk.Align.CENTER)

        self.set_valign(Gtk.Align.CENTER)

        self.set_margin_top(30)

        self.set_margin_bottom(30)

        self.set_margin_start(30)

        self.set_margin_end(30)

        # Title
        title = Gtk.Label(label="Transfer Money")

        title.add_css_class("title-1")

        subtitle = Gtk.Label(

           label="Send money to another SynapseCash account."
        )
        subtitle.add_css_class("dim-label")

        # Recipient account number

        account_label = Gtk.Label(label="Recipient Account Number")

        account_label.set_halign(Gtk.Align.START)

        self.account_entry = Gtk.Entry()

        self.account_entry.set_placeholder_text(

            "Enter 12-digit account number"
        )
        self.account_entry.set_size_request(280, 42)

        self.account_entry.set_max_length(12)

        # Transfer amount
        amount_label = Gtk.Label(label="Transfer Amount")

        amount_label.set_halign(Gtk.Align.START)

        self.amount_entry = Gtk.Entry()

        self.amount_entry.set_placeholder_text("Enter amount")

        self.amount_entry.set_size_request(280, 42)

        self.amount_entry.set_input_purpose(
            Gtk.InputPurpose.NUMBER
        )

        # Status message
        self.status_label = Gtk.Label(label="")

        self.status_label.set_wrap(True)

        self.status_label.add_css_class("danger")

        # Transfer button
        transfer_button = CustomButton("Confirm Transfer")

        transfer_button.set_size_request(280, 45)

        transfer_button.connect(

            "clicked",

            self.handle_transfer
        )

        # Back button

        back_button = Gtk.Button(label="Back")

        back_button.set_size_request(280, 40)


        if on_back is not None:

            back_button.connect("clicked", on_back)


        # Add widgets

        self.append(title)

        self.append(subtitle)

        self.append(account_label)

        self.append(self.account_entry)

        self.append(amount_label)

        self.append(self.amount_entry)

        self.append(transfer_button)

        self.append(self.status_label)

        self.append(back_button)

    def handle_transfer(self, button):

        """Validate transfer details and call the callback."""

        account_number = self.account_entry.get_text().strip()

        amount_text = self.amount_entry.get_text().strip()

        if not account_number or not amount_text:

            self.show_error("Please complete all fields.")

            return

        if not account_number.isdigit() or len(account_number) != 12:

            self.show_error(

                "Account number must contain exactly 12 digits."
            )

            return

        try:

            amount = Decimal(amount_text)

            if not amount.is_finite():

                raise InvalidOperation

            amount = amount.quantize(Decimal("0.01"))

        except (InvalidOperation, ValueError):

            self.show_error("Please enter a valid amount.")

            return

        if amount <= Decimal("0.00"):

            self.show_error("Amount must be greater than zero.")

            return

        self.status_label.set_text("")

        if self.on_transfer is not None:

            self.on_transfer(account_number, amount)

    def show_error(self, message):
        
        """Display a transfer error."""

        self.status_label.set_text(message)
