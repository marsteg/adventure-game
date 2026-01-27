import pygame


class RectShape(pygame.sprite.Sprite):
    """Base class for rectangular game objects (Items, Doors, Actions, NPCs)."""

    def __init__(self, left, top, width, height, image):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.velocity = pygame.Vector2(0, 0)
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.image = image

    def draw(self, screen):
        """Override in subclasses to draw the object."""
        pass

    def update(self, dt):
        """Override in subclasses to update the object."""
        pass

    def kill(self, arg1, arg2):
        """Override in subclasses to handle object destruction."""
        pass

    def collides_with(self, other):
        """Check if this object collides with another."""
        return self.rect.colliderect(other.rect)

    def collidepoint(self, pos):
        """Check if a point is within this object's rect."""
        return self.rect.collidepoint(pos)

    def shine(self, screen):
        """Draw a highlight overlay on the object."""
        shiner = pygame.Surface((self.rect.width, self.rect.height))
        shiner.fill((255, 255, 255))
        shiner.set_alpha(100)
        screen.blit(shiner, self.rect.topleft)
