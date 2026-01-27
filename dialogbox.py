import pygame
import wave
import contextlib


class DialogBox(pygame.sprite.Sprite):
    """A text box that displays dialog on screen."""
    containers = []
    dialogboxes = []

    def __init__(self, room, time):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.timer = time
        self.state = None
        self.room = room
        self.surface = None
        self.rect = None
        DialogBox.dialogboxes.append(self)

    def draw(self, screen):
        if self.surface and self.rect:
            screen.blit(self.surface, self.rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos) if self.rect else False

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
