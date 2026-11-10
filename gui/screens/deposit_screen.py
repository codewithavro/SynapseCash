
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gui.components.custom_button import CustomButton


class DepositScreen(Gtk.Box):
    """Deposit money screen for SynapseCash."""

    def __init__(self, on_deposit=None, on_back=None):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=15
        )

        self.on_deposit = on_deposit

        # Screen layout
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_margin_top(30)
        self.set_margin_bottom(30)
        self.set_margin_start(30)
        self.set_margin_end(30)

        # Title
        title = Gtk.Label(label="Deposit Money")
        title.add_css_class("title-1")

        subtitle = Gtk.Label(
            label="Add money to your SynapseCash account."
        )
        subtitle.add_css_class("dim-label")

        # Amount field
        amount_label = Gtk.Label(label="Deposit Amount")
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

        # Deposit button
        deposit_button = CustomButton("Confirm Deposit")
        deposit_button.set_size_request(280, 45)
        deposit_button.connect(
            "clicked",
            self.handle_deposit
        )

        # Back button
        back_button = Gtk.Button(label="Back")
        back_button.set_size_request(280, 40)

        if on_back is not None:
            back_button.connect("clicked", on_back)

        # Add widgets
        self.append(title)
        self.append(subtitle)
        self.append(amount_label)
        self.append(self.amount_entry)
        self.append(deposit_button)
        self.append(self.status_label)
        self.append(back_button)

    def handle_deposit(self, button):
        """Validate the amount and call the deposit callback."""

        amount_text = self.amount_entry.get_text().strip()

        if not amount_text:
            self.show_error("Please enter a deposit amount.")
            return

        try:
            amount = float(amount_text)

        except ValueError:
            self.show_error("Please enter a valid amount.")
            return

        if amount <= 0:
            self.show_error("Amount must be greater than zero.")
            return

        self.status_label.set_text("")

        if self.on_deposit is not None:
            self.on_deposit(amount)

    def show_error(self, message):
        """Display a deposit error."""

        self.status_label.set_text(message)
