
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from gui.components.audio_player import AudioPlayer


# Shared audio player for button clicks
_audio_player = AudioPlayer()


class CustomButton(Gtk.Button):
    """Reusable button for the SynapseCash application."""

    def __init__(self, label, on_click=None):
        super().__init__(label=label)

        self.add_css_class("custom-button")

        self.on_click_callback = on_click

        self.connect("clicked", self.handle_click)

    def handle_click(self, button):
        """Play the click sound and execute the button callback."""

        try:
            _audio_player.play("button_click.ogg")
        except Exception:
            pass

        if self.on_click_callback is not None:
            self.on_click_callback(button)
