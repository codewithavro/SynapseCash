
import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class SummaryCard(Gtk.Frame):
    """Reusable information card for the SynapseCash dashboard."""

    def __init__(self, title, value, subtitle=""):
        super().__init__()

        # Apply card styling
        self.add_css_class("card")

        # Create the card layout
        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        content.set_margin_top(16)
        content.set_margin_bottom(16)
        content.set_margin_start(16)
        content.set_margin_end(16)

        # Card title
        title_label = Gtk.Label(label=title)
        title_label.set_xalign(0)
        title_label.add_css_class("heading")

        # Main value
        value_label = Gtk.Label(label=str(value))
        value_label.set_xalign(0)
        value_label.add_css_class("title-1")

        # Supporting text
        subtitle_label = Gtk.Label(label=subtitle)
        subtitle_label.set_xalign(0)
        subtitle_label.add_css_class("dim-label")

        # Add labels to the card
        content.append(title_label)
        content.append(value_label)
        content.append(subtitle_label)

        self.set_child(content)
