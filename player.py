import pygame


def load_image(path, width, height):
    """Load and scale an image with transparency."""
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    return image


class Player(pygame.sprite.Sprite):
    """The player character with walking animation."""
    _id_counter = 1
    containers = []

    def __init__(self, left, top, width, height, image, name):
        super().__init__()
        self.pos = pygame.Vector2(left, top)
        self.rect = pygame.Rect(left, top, width, height)
        self.defaultimage = load_image(image, width, height)
        self.name = name
        self.speed = 5
        self.target = self.pos.copy()

        # Load walking animation sprites
        self.rightsprites = [
            load_image(f"assets/player/walking/right{i}.png", width, height)
            for i in range(6)
        ]
        self.leftsprites = [
            load_image(f"assets/player/walking/left{i}.png", width, height)
            for i in range(6)
        ]
        self.current_sprite = 0.0
        self.image = self.defaultimage

    def set_target(self, pos):
        """Set a target position for the player to walk to."""
        px, py = pos
        # Center the player on the click position
        newpos = px - self.rect.width // 2, py - self.rect.height
        self.target = pygame.Vector2(newpos)

    def clear_target(self):
        """Stop the player's movement."""
        self.target = self.pos.copy()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        # Animate walking
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.rightsprites):
            self.current_sprite = 0.0

        # Update sprite based on movement direction
        if self.target == self.pos:
            self.image = self.defaultimage
        elif self.target.x > self.pos.x:
            self.image = self.rightsprites[int(self.current_sprite)]
        elif self.target.x < self.pos.x:
            self.image = self.leftsprites[int(self.current_sprite)]

        # Move towards target
        move = self.target - self.pos
        move_length = move.length()

        if move_length < self.speed:
            self.pos = self.target.copy()
        elif move_length > 0:
            move.normalize_ip()
            self.pos += move * self.speed

        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
