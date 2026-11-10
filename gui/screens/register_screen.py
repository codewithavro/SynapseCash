import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gui.components.custom_button import CustomButton

class RegisterScreen(Gtk.Box):

    """Registration screen for SynapseCash"""

    def __init__(self, on_register=None, on_back=None):

        super().__init__(

            orientation=Gtk.Orientation.VERTICAL,

            spacing=12

        )

        self.on_register = on_register

        # Screen Layout

        self.set_halign(Gtk.Align.CENTER)

        self.set_valign(Gtk.Align.CENTER)

        self.set_margin_top(30)

        self.set_margin_bottom(30)

        self.set_margin_start(30)

        self.set_margin_end(30)

       # Screen title
        title = Gtk.Label(label="Create Your Account")
        title.add_css_class("title-1")

        subtitle = Gtk.Label(
            label="Join SynapseCash and manage your finances."
        )
        subtitle.add_css_class("dim-label")

        # Full name
        self.full_name_entry = self.create_entry(
            "Enter your full name"
        )
        self.add_field("Full Name", self.full_name_entry)

        # Username
        self.username_entry = self.create_entry(
            "Choose a username"
        )
        self.add_field("Username", self.username_entry)

        # PIN
        self.pin_entry = self.create_entry("Enter 6-digit PIN")

        self.pin_entry.set_visibility(False)

        self.pin_entry.set_max_length(6)

        self.pin_entry.set_input_purpose(Gtk.InputPurpose.PIN)

        self.add_field("6-Digit PIN", self.pin_entry)

        # Confirm PIN
        self.confirm_pin_entry = self.create_entry(
            "Confirm your PIN"
        )

        self.confirm_pin_entry.set_visibility(False)

        self.confirm_pin_entry.set_max_length(6)

        self.confirm_pin_entry.set_input_purpose(
            Gtk.InputPurpose.PIN
        )

        self.add_field("Confirm PIN", self.confirm_pin_entry)


        # Status message
        self.status_label = Gtk.Label(label="")

        self.status_label.set_wrap(True)

        self.status_label.add_css_class("danger")

        # Register button
        register_button = CustomButton("Create Account")

        register_button.set_size_request(280, 45)

        register_button.connect(

            "clicked",

            self.handle_register
        )

        # Back button

        back_button = Gtk.Button(label="Back")

        back_button.set_size_request(280, 40)

        if on_back is not None:

            back_button.connect("clicked", on_back)

        # Add widgets

        self.append(title)

        self.append(subtitle)

        self.append(self.full_name_entry.field_container)

        self.append(self.username_entry.field_container)

        self.append(self.pin_entry.field_container)
        
        self.append(self.confirm_pin_entry.field_container)

        self.append(register_button)

        self.append(self.status_label)

        self.append(back_button) 

    def create_entry(self, placeholder):
        """Create a standard input field."""

        entry = Gtk.Entry()
        entry.set_placeholder_text(placeholder)
        entry.set_size_request(280, 40)

        return entry 
    
    def add_field(self, label_text, entry):
        """Create a labeled input field."""

        container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=5
        )

        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)

        container.append(label)
        container.append(entry)

        # Store the container on the entry for layout access
        entry.field_container = container

    def handle_register(self, button):
        """Validate registration input and call the callback."""

        full_name = self.full_name_entry.get_text().strip()
        username = self.username_entry.get_text().strip()
        pin = self.pin_entry.get_text()
        confirm_pin = self.confirm_pin_entry.get_text()

        if not all([full_name, username, pin, confirm_pin]):
            self.show_error("Please complete all fields.")
            return

        if not pin.isdigit() or len(pin) != 6:
            self.show_error("PIN must contain exactly 6 digits.")
            return

        if pin != confirm_pin:
            self.show_error("PIN entries do not match.")
            return

        self.status_label.set_text("")

        if self.on_register is not None:
            self.on_register(
                full_name,
                username,
                pin,
                confirm_pin
            )

    def show_error(self, message):
        """Display a registration error."""

        self.status_label.set_text(message)




        

    

