import pygame
import wave
import contextlib


class VoiceManager:
    """Centralized voice management system to prevent overlapping audio."""
    current_sound = None
    current_channel = None

    @classmethod
    def play_voice(cls, sound_file):
        """Play a voice line, stopping any currently playing voice."""
        cls.stop_current_voice()

        try:
            sound = pygame.mixer.Sound(sound_file)
            # Use a dedicated channel for voice to separate from music/effects
            cls.current_channel = pygame.mixer.Channel(0)  # Reserve channel 0 for voice
            cls.current_channel.play(sound)
            cls.current_sound = sound
            print(f"Playing voice: {sound_file}")
        except Exception as e:
            print(f"Error playing voice {sound_file}: {e}")

    @classmethod
    def stop_current_voice(cls):
        """Stop any currently playing voice."""
        if cls.current_channel and cls.current_channel.get_busy():
            cls.current_channel.stop()
            print("Voice stopped")
        cls.current_sound = None
        cls.current_channel = None

    @classmethod
    def is_voice_playing(cls):
        """Check if a voice line is currently playing."""
        return cls.current_channel and cls.current_channel.get_busy()


class DialogBox(pygame.sprite.Sprite):
    """A text box that displays dialog on screen using the new UI renderer."""
    containers = []
    dialogboxes = []

    def __init__(self, room, time):
        #pygame.sprite.Sprite.__init__(self, self.containers)
        pygame.sprite.Sprite.__init__(self)
        self.timer = time
        self.state = None
        self.room = room
        # Store dialog text and speaker info for new renderer
        self.dialog_text = ""
        self.speaker_name = ""
        self.speaker_color = None
        DialogBox.dialogboxes.append(self)

    def kill(self):
        if self in DialogBox.dialogboxes:
            DialogBox.dialogboxes.remove(self)
        pygame.sprite.Sprite.kill(self)
        print("DialogBox removed")


def get_sound_duration(sound_path):
    """Get the duration of a WAV sound file in seconds."""
    try:
        with contextlib.closing(wave.open(sound_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            print(f"Sound duration: {duration:.2f}s")
            return duration
    except (wave.Error, FileNotFoundError) as e:
        print(f"Error reading sound file {sound_path}: {e}")
        return 3.0  # Default duration
