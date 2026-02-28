import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT, BACKGROUND_VOLUME
from dialogbox import DialogBox
from ui import dialog_renderer


class Room(pygame.sprite.Sprite):
    _id_counter = 1
    containers = []
    rooms = {}
    _image_cache = {}  # Cache for loaded images

    def __init__(self, player, image, name, music, walkable_mask=None):
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

        # Walkable area mask
        self.walkable_mask = None
        if walkable_mask:
            self._load_walkable_mask(walkable_mask)

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

    def draw_walkable_overlay(self, screen):
        """Draw a semi-transparent overlay showing walkable areas (for debugging)."""
        if not self.walkable_mask:
            return

        # Create a semi-transparent overlay
        overlay = self.walkable_mask.copy()
        overlay.set_alpha(120)  # Semi-transparent
        # Tint it green for visibility
        overlay.fill((0, 255, 0, 120), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(overlay, self.rect)

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

    def _load_walkable_mask(self, mask_path):
        """Load and cache the walkable area mask image."""
        try:
            mask_img = pygame.image.load(mask_path).convert_alpha()
            self.walkable_mask = pygame.transform.scale(
                mask_img,
                (SCREEN_WIDTH, SCREEN_HEIGHT - INVENTORY_HEIGHT)
            )
            print(f"Loaded walkable mask for room '{self.name}': {mask_path}")
        except Exception as e:
            print(f"Warning: Could not load walkable mask '{mask_path}' for room '{self.name}': {e}")
            self.walkable_mask = None

    def is_walkable(self, pos):
        """Check if a position is walkable in this room.

        Args:
            pos: Tuple (x, y) position to check

        Returns:
            bool: True if walkable, False if blocked
        """
        if not self.walkable_mask:
            # No mask = everywhere is walkable (backward compatible)
            return True

        x, y = int(pos[0]), int(pos[1])

        # Check bounds
        if not (0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT - INVENTORY_HEIGHT):
            return False

        # Check mask pixel - white/visible = walkable, black/transparent = non-walkable
        try:
            color = self.walkable_mask.get_at((x, y))
            # Consider pixel walkable if it has high alpha (visible)
            return color.a > 128
        except IndexError:
            # Out of bounds = not walkable
            return False

    def find_nearest_walkable(self, pos):
        """Find the nearest walkable point to a given position.

        Args:
            pos: Tuple (x, y) target position

        Returns:
            Tuple (x, y) of nearest walkable position, or original pos if no mask
        """
        if not self.walkable_mask:
            return pos

        if self.is_walkable(pos):
            return pos

        # Spiral search outward from the target position
        import math
        x, y = int(pos[0]), int(pos[1])
        max_search_radius = 200  # Don't search too far

        for radius in range(1, max_search_radius, 5):
            # Check points in a circle around the target
            for angle in range(0, 360, 15):  # Check every 15 degrees
                check_x = int(x + radius * math.cos(math.radians(angle)))
                check_y = int(y + radius * math.sin(math.radians(angle)))

                if self.is_walkable((check_x, check_y)):
                    return (check_x, check_y)

        # If no walkable point found, return original (player won't move)
        return pos

    def find_nearest_walkable_spawn(self, spawn_pos, player_width=50, player_height=75):
        """Find nearest valid spawn position where player's FEET will be walkable.

        This is specifically for door spawns. It ensures that when a player spawns
        at the returned position, their feet (spawn + (width/2, height)) will be
        on a walkable area.

        Args:
            spawn_pos: Tuple (x, y) desired spawn position (top-left of player)
            player_width: Width of player sprite (default 50)
            player_height: Height of player sprite (default 75)

        Returns:
            Tuple (x, y) of valid spawn position where feet will be walkable
        """
        if not self.walkable_mask:
            return spawn_pos

        # Calculate where feet would be from this spawn
        feet_x = int(spawn_pos[0] + player_width // 2)
        feet_y = int(spawn_pos[1] + player_height)

        # If feet are already walkable, use this spawn
        if self.is_walkable((feet_x, feet_y)):
            return spawn_pos

        # Otherwise, search for a spawn where feet WILL be walkable
        import math
        x, y = int(spawn_pos[0]), int(spawn_pos[1])
        max_search_radius = 200

        for radius in range(1, max_search_radius, 5):
            for angle in range(0, 360, 15):
                check_spawn_x = int(x + radius * math.cos(math.radians(angle)))
                check_spawn_y = int(y + radius * math.sin(math.radians(angle)))

                # Calculate where feet would be from this spawn
                check_feet_x = check_spawn_x + player_width // 2
                check_feet_y = check_spawn_y + player_height

                # Check if feet position is walkable
                if self.is_walkable((check_feet_x, check_feet_y)):
                    return (check_spawn_x, check_spawn_y)

        # If no valid spawn found, return original
        return spawn_pos
