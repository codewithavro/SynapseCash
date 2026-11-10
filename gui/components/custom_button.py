
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class CustomButton(Gtk.Button):
    """Reusable button for the SynapseCash application."""

    def __init__(self, label, on_click=None):
        super().__init__(label=label)

        # Apply the custom button style
        self.add_css_class("custom-button")

        # Connect the click event if provided
        if on_click is not None:
            self.connect("clicked", on_click)
