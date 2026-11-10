
import gi
from pathlib import Path

gi.require_version("Gst", "1.0")

from gi.repository import Gst


# Initialize GStreamer
Gst.init(None)


class AudioPlayer:
    """Manage SynapseCash audio playback."""

    def __init__(self):
        self.player = Gst.ElementFactory.make("playbin", "audio-player")

        if self.player is None:
            raise RuntimeError("Unable to create GStreamer audio player.")

        self.sounds_folder = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "sounds"
        )

    def play(self, filename):
        """Play an OGG sound file."""

        if Path(filename).name != filename:
            raise ValueError("Only sound filenames are allowed.")

        sound_path = self.sounds_folder / filename

        if not sound_path.is_file():
            raise FileNotFoundError(
                f"Sound file not found: {sound_path}"
            )

        # Stop any previous sound
        self.player.set_state(Gst.State.NULL)

        # Set the audio file
        self.player.set_property(
            "uri",
            sound_path.resolve().as_uri()
        )

        # Start playback
        result = self.player.set_state(Gst.State.PLAYING)

        if result == Gst.StateChangeReturn.FAILURE:
            raise RuntimeError("Unable to start audio playback.")

    def stop(self):
        """Stop audio playback."""

        self.player.set_state(Gst.State.NULL)

    def set_volume(self, volume):
        """Set volume between 0.0 and 1.0."""

        if not isinstance(volume, (int, float)):
            raise TypeError("Volume must be a number.")

        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0.")

        self.player.set_property("volume", volume)
