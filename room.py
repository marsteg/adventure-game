import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT, BACKGROUND_VOLUME
from dialogbox import DialogBox
from ui import dialog_renderer


class Room(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    rooms = {}
    _image_cache = {}  # Cache for loaded images

    def __init__(self, player, image, name, music):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - INVENTORY_HEIGHT)
        self.id = Room._id_counter
        Room._id_counter += 1
        self.doors = {}
        self.items = {}
        self.actions = {}
        self.npcs = {}
        self.name = name
        self.music = music
        self.player = player
        Room.rooms[self.name] = self
        self._cached_image = None
        self._cached_imagepath = None
        self.imagepath = image
        self.image = pygame.image.load(self.imagepath).convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT - INVENTORY_HEIGHT))

    def _load_image(self):
        """Load and cache the image. Only reload if path changed."""
        if self._cached_imagepath != self.imagepath:
            cache_key = (self.imagepath, self.rect.width, self.rect.height)
            if cache_key not in Room._image_cache:
                img = pygame.image.load(self.imagepath).convert_alpha()
                img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
                Room._image_cache[cache_key] = img
            self._cached_image = Room._image_cache[cache_key]
            self._cached_imagepath = self.imagepath

    def draw(self, screen, inventory, answerbox):
        self._load_image()
        screen.blit(self._cached_image, self.rect)

        for door in self.doors.values():
            door.draw(screen)
        for action in self.actions.values():
            action.draw(screen)
        for npc in self.npcs.values():
            npc.draw(screen)
        for item in self.items.values():
            item.draw(screen)
        self.player.draw(screen)

        # Clear previous speech tracking and draw dialogs with new direct text renderer
        dialog_renderer.clear_all_speeches()

        # Only show the most recent dialog per speaking NPC to prevent overlapping sentences
        npc_to_latest_dialog = {}
        for dialogbox in DialogBox.dialogboxes:
            if dialogbox.room == self and dialogbox.dialog_text:
                speaking_npc = getattr(dialogbox, 'speaking_npc', None)
                if speaking_npc:
                    # Keep only the most recent dialog per NPC (highest timer = most recent)
                    if speaking_npc not in npc_to_latest_dialog or dialogbox.timer > npc_to_latest_dialog[speaking_npc].timer:
                        npc_to_latest_dialog[speaking_npc] = dialogbox

        # Render only the latest dialog for each NPC
        for speaking_npc, dialogbox in npc_to_latest_dialog.items():
            speaker_name = getattr(dialogbox, 'speaker_name', "")
            speaker_color = getattr(dialogbox, 'speaker_color', None)
            dialog_renderer.render_dialog_text(screen, dialogbox.dialog_text, speaking_npc,
                                             speaker_name=speaker_name, speaker_color=speaker_color)

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
