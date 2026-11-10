import gi
from pathlib import Path

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gui.components.custom_button import CustomButton

# Locate the project assets folder

BASE_DIR = Path(__file__).resolve().parents[2]
LOGO_PATH = BASE_DIR / "assets" / "images" / "logo" / "logo.png"

class WelcomeScreen(Gtk.Box):
    """Welcome screen for the SynapseCash application"""

    def __int__(self, on_login=None, on_register=None):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=18
        )

        # Main layout settings

        self.set_halign(Gtk.Align.CENTER)

        self.set_valign(Gtk.Align.CENTER)

        self.set_margin_top(40)

        self.set_margin_bottom(40)

        self.set_margin_start(30)

        self.set_margin_end(30)

        # Display the application logo

        if LOGO_PATH.is_file():

            logo = Gtk.Picture.new_for_filename(str(LOGO_PATH))

            logo.set_content_fit(Gtk.ContentFit.CONTAIN)

            logo.set_size_request(160, 160)

            logo.set_halign(Gtk.Align.CENTER)

            self.append(logo)

            # Application name

            title = Gtk.Label(label="SynapseCash")

            title.add_css_class("title-1")

            title.set_halign(Gtk.Align.CENTER)

            # Welcome message

            subtitle = Gtk.Label(

                label="Your Money. Your Control. Your Security"
            )

            subtitle.set_halign(Gtk.Align.CENTER)

            subtitle.add_css_class("dim-label")

            # Intrduction

            description = Gtk.Label(

                label="Welcome to your personal ATM simulator."
            )

            description.set_halign(Gtk.Align.CENTER)

            # Login button

            login_button = CustomButton(

                "Login",
                on_login
            )
            login_button.set_size_request(220, 45)

            #Registration button

            register_button = CustomButton(

                "Create New Account",
                on_register
            )

            register_button.set_size_request(220, 45)

            # Add components to the screen

            self.append(title)

            self.append(subtitle)

            self.append(description)

            self.append(login_button)

            self.append(register_button)


