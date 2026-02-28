#!/usr/bin/env python3
"""Visualize walkable mask to debug issues."""

import pygame
import sys

pygame.init()

# Import constants
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT

# Check if mask path provided
if len(sys.argv) < 2:
    print("Usage: python visualize_mask.py <mask_path>")
    print("Example: python visualize_mask.py assets/rooms/TitleScreen_mask.png")
    sys.exit(1)

mask_path = sys.argv[1]

# Load mask
try:
    mask = pygame.image.load(mask_path).convert_alpha()
    print(f"Original mask size: {mask.get_size()}")
except Exception as e:
    print(f"Error loading mask: {e}")
    sys.exit(1)

# Scale to game size
target_size = (SCREEN_WIDTH, SCREEN_HEIGHT - INVENTORY_HEIGHT)
mask_scaled = pygame.transform.scale(mask, target_size)
print(f"Scaled to: {target_size}")

# Analyze mask
walkable_pixels = 0
blocked_pixels = 0
for y in range(target_size[1]):
    for x in range(target_size[0]):
        alpha = mask_scaled.get_at((x, y)).a
        if alpha > 128:
            walkable_pixels += 1
        else:
            blocked_pixels += 1

total_pixels = walkable_pixels + blocked_pixels
walkable_percent = (walkable_pixels / total_pixels) * 100
print(f"\nAnalysis:")
print(f"  Walkable pixels: {walkable_pixels} ({walkable_percent:.1f}%)")
print(f"  Blocked pixels: {blocked_pixels} ({100-walkable_percent:.1f}%)")

if walkable_percent < 10:
    print("\n⚠️  WARNING: Less than 10% of the area is walkable!")
    print("   Your mask might be inverted or mostly blocked.")
elif walkable_percent > 90:
    print("\n⚠️  WARNING: More than 90% of the area is walkable!")
    print("   Your mask might not have any obstacles defined.")

# Create visualization window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"Walkable Mask Viewer: {mask_path}")

# Create overlay
overlay = pygame.Surface(target_size, pygame.SRCALPHA)
for y in range(target_size[1]):
    for x in range(target_size[0]):
        alpha = mask_scaled.get_at((x, y)).a
        if alpha > 128:
            # Walkable - green
            overlay.set_at((x, y), (0, 255, 0, 120))
        else:
            # Blocked - red
            overlay.set_at((x, y), (255, 0, 0, 120))

print("\n" + "="*60)
print("Displaying mask visualization...")
print("  GREEN = Walkable (alpha > 128)")
print("  RED = Blocked (alpha ≤ 128)")
print("\nMove mouse to see pixel details")
print("Press SPACE to toggle overlay")
print("Press ESC to quit")
print("="*60)

show_overlay = True
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                show_overlay = not show_overlay
                status = "ON" if show_overlay else "OFF"
                print(f"Overlay: {status}")

    # Clear screen
    screen.fill((0, 0, 0))

    # Show original mask (as background)
    screen.blit(mask_scaled, (0, 0))

    # Show overlay
    if show_overlay:
        screen.blit(overlay, (0, 0))

    # Show mouse position and pixel info
    mouse_pos = pygame.mouse.get_pos()
    if 0 <= mouse_pos[0] < SCREEN_WIDTH and 0 <= mouse_pos[1] < target_size[1]:
        pixel_alpha = mask_scaled.get_at(mouse_pos).a
        is_walkable = "WALKABLE" if pixel_alpha > 128 else "BLOCKED"
        color = (0, 255, 0) if pixel_alpha > 128 else (255, 0, 0)

        # Draw crosshair
        pygame.draw.line(screen, color, (mouse_pos[0] - 10, mouse_pos[1]), (mouse_pos[0] + 10, mouse_pos[1]), 2)
        pygame.draw.line(screen, color, (mouse_pos[0], mouse_pos[1] - 10), (mouse_pos[0], mouse_pos[1] + 10), 2)

        # Draw info text
        font = pygame.font.Font(None, 24)
        info_text = f"({mouse_pos[0]}, {mouse_pos[1]}) alpha={pixel_alpha} {is_walkable}"
        text_surf = font.render(info_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(topleft=(10, 10))
        # Background for text
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(10, 10))
        screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
