import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gui.components.custom_button import CustomButton

class LoginScreen(Gtk.Box):
    """Login screen for SynapseCash"""

    def __init__(self, on_login=None, on_back=None):
        super().__init__(

            orientation=Gtk.Orientation.VERTICAL,

            spacing=15
            
            )

        # Screen Layout

        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_margin_top(40)
        self.set_margin_bottom(40)
        self.set_margin_start(30)
        self.set_margin_end(30)


        # Screen title
        title = Gtk.Label(label="Welcome Back")
        title.add_css_class("title-1")

        subtitle = Gtk.Label(
            label="Log in to your SynapseCash account."
        )
        subtitle.add_css_class("dim-label")

        # Username field
        username_label = Gtk.Label(label="Username")
        username_label.set_halign(Gtk.Align.START)

        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Enter your username")
        self.username_entry.set_size_request(280, 42)

        # PIN field
        pin_label = Gtk.Label(label="6-Digit PIN")
        pin_label.set_halign(Gtk.Align.START)

        self.pin_entry = Gtk.Entry()
        self.pin_entry.set_placeholder_text("Enter your PIN")
        self.pin_entry.set_visibility(False)
        self.pin_entry.set_max_length(6)
        self.pin_entry.set_input_purpose(
            Gtk.InputPurpose.PIN
        )
        self.pin_entry.set_size_request(280, 42)

        # Status message
        self.status_label = Gtk.Label(label="")
        self.status_label.set_wrap(True)
        self.status_label.add_css_class("danger")

        # Login button
        login_button = CustomButton("Login")
        login_button.set_size_request(280, 45)
        login_button.connect(
            "clicked",
            self.handle_login,
            on_login
        )

        # Back button
        back_button = Gtk.Button(label="Back")
        back_button.set_size_request(280, 40)

        if on_back is not None:
            back_button.connect("clicked", on_back)

        # Add widgets
        self.append(title)
        self.append(subtitle)
        self.append(username_label)
        self.append(self.username_entry)
        self.append(pin_label)
        self.append(self.pin_entry)
        self.append(login_button)
        self.append(self.status_label)
        self.append(back_button)

    def handle_login(self, button, on_login):
        """Handle the login button click."""

        username = self.username_entry.get_text().strip()
        pin = self.pin_entry.get_text()

        if not username or not pin:
            self.status_label.set_text(
                "Please enter your username and PIN."
            )
            return

        if not pin.isdigit() or len(pin) != 6:
            self.status_label.set_text(
                "PIN must contain exactly 6 digits."
            )
            return

        self.status_label.set_text("")

        if on_login is not None:
            on_login(username, pin)

