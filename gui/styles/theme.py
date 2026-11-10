import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gdk

from gui.styles import colors

def apply_theme():
    """Apply the SynapseCash GTK 4 visual theme"""

css = f"""
window {{
    background-color: {colors.BACKGROUND};
    color: {colors.TEXT_PRIMARY};
}}

label {{
    color: {colors.TEXT_PRIMARY};
}}

button {{
    background-color: {colors.SECONDARY};
    color: {colors.TEXT_LIGHT};
    border-radius: 8px;
    padding: 10px;
}}

button:hover {{
    background-color: {colors.PRIMARY};
}}

entry {{
    background-color: {colors.CARD_BACKGROUND};
    color: {colors.TEXT_PRIMARY};
    border-radius: 8px;
    padding: 10px;
}}

.card {{
    background-color: {colors.CARD_BACKGROUND};
    border-radius: 12px;
    padding: 16px;
}}

.success {{
    color: {colors.SUCCESS};
}}

.danger {{
    color: {colors.DANGER};
}}
"""

provider = Gtk.CssProvider()

provider.load_from_data(css.encode("utf-8"))

display = Gdk.Display.get_default()

if display is None:
        raise RuntimeError("N GTK diplay is available")

Gtk.StyleContext.add_provider_for_display(

        display,

        provider,

        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )