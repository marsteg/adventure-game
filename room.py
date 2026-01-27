import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT, BACKGROUND_VOLUME
from dialogbox import DialogBox
from ui import dialog_renderer


class Room(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    rooms = {}

    def __init__(self, player, image, name, music):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - INVENTORY_HEIGHT)
        self.id = Room._id_counter
        Room._id_counter += 1
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT - INVENTORY_HEIGHT))
        self.doors = {}
        self.items = {}
        self.actions = {}
        self.npcs = {}
        self.name = name
        self.music = music
        self.player = player
        Room.rooms[self.name] = self

    def draw(self, screen, inventory, answerbox):
        screen.blit(self.image, self.rect)

        for door in self.doors.values():
            door.draw(screen)
        for action in self.actions.values():
            action.draw(screen)
        for npc in self.npcs.values():
            npc.draw(screen)
        for item in self.items.values():
            item.draw(screen)
        self.player.draw(screen)

        # Draw dialogs with new renderer
        for dialogbox in DialogBox.dialogboxes:
            if dialogbox.room == self and dialogbox.surface:
                # Extract text from the rendered surface or use stored text
                if hasattr(dialogbox, 'dialog_text') and dialogbox.dialog_text:
                    speaker = getattr(dialogbox, 'speaker_name', "")
                    dialog_renderer.render_dialog_box(screen, dialogbox.dialog_text, speaker_name=speaker)
                else:
                    # Fallback: draw old style if no text stored
                    dialogbox.draw(screen)

        # Inventory/answerbox drawn by main.py with new renderers

    def play(self):
        print("Playing music: ", self.music)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
        pygame.mixer.music.play(-1, 0.0)

    def shine(self, screen):
        """Highlight all interactive objects in the room."""
        for item in self.items.values():
            item.shine(screen)
        for door in self.doors.values():
            door.shine(screen)
        for action in self.actions.values():
            action.shine(screen)
        for npc in self.npcs.values():
            npc.shine(screen)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, dt):
        pass
