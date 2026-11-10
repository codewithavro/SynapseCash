
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gui.components.custom_button import CustomButton

from transactions.transaction_history import get_transaction_history


class HistoryScreen(Gtk.Box):

    """Transaction history screen for SynapseCash."""

    def __init__(self, user_id, on_back=None):

        super().__init__(

            orientation=Gtk.Orientation.VERTICAL,

            spacing=15
        )

        self.user_id = user_id

        # Screen layout

        self.set_margin_top(25)

        self.set_margin_bottom(25)

        self.set_margin_start(25)

        self.set_margin_end(25)

        # Title
        title = Gtk.Label(label="Transaction History")

        title.add_css_class("title-1")

        title.set_halign(Gtk.Align.START)

        subtitle = Gtk.Label(

            label="Review your recent account "
            "transactions."
        )
        subtitle.add_css_class("dim-label")

        subtitle.set_halign(Gtk.Align.START)

        # Transaction list

        self.transaction_list = Gtk.ListBox()

        self.transaction_list.set_selection_mode(

            Gtk.SelectionMode.NONE
        )

        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(

            Gtk.PolicyType.AUTOMATIC,

            Gtk.PolicyType.AUTOMATIC
        )
        scroll.set_min_content_height(300)

        scroll.set_child(self.transaction_list)

        scroll.set_vexpand(True)


        # Status message
        self.status_label = Gtk.Label(label="")

        self.status_label.set_wrap(True)

        # Back button
        back_button = Gtk.Button(label="Back")

        back_button.set_size_request(180, 40)

        if on_back is not None:

            back_button.connect("clicked", on_back)

        # Add widgets
        self.append(title)

        self.append(subtitle)

        self.append(scroll)

        self.append(self.status_label)

        self.append(back_button)

        # Load transaction history

        self.load_history()

    def load_history(self):

        """Load and display recent transactions."""

        try:
            transactions = get_transaction_history(

                self.user_id,

                limit=50
            )

            if not transactions:

                self.status_label.set_text(

                    "No transactions found."
                )
                return

            for transaction in transactions:

                transaction_type = transaction
                ["transaction_type"]

                amount = transaction["amount"]

                balance = transaction["balance_after"]

                date = transaction["created_at"]

                row_text = (

                    f"{transaction_type}  |  "

                    f"Amount: {amount}  |  "

                    f"Balance: {balance}  |  "

                    f"{date}"
                )

                label = Gtk.Label(label=row_text)

                label.set_halign(Gtk.Align.START)

                label.set_wrap(True)

                label.set_margin_top(8)

                label.set_margin_bottom(8)

                label.set_margin_start(8)

                label.set_margin_end(8)

                self.transaction_list.append(label)


            self.status_label.set_text(

                f"Showing {len(transactions)} recent transactions."
            )

        except Exception:

            self.status_label.set_text(
                
                "Unable to load transaction history."
            )
