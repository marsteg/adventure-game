#!/usr/bin/env python3
"""
Example script to create a walkable area mask.

This script demonstrates how to create a simple walkable mask programmatically.
For real game development, you should create masks using image editing software
like Photoshop, GIMP, or Krita for better control.
"""

import pygame
import sys
import os

def create_example_mask(width=1280, height=666, output_path="example_mask.png"):
    """
    Create an example walkable area mask.

    This creates a simple mask with:
    - A rectangular walkable floor area in the center
    - Margins around edges (non-walkable, like walls)

    Args:
        width: Mask width (default 1280 = SCREEN_WIDTH)
        height: Mask height (default 666 = SCREEN_HEIGHT - INVENTORY_HEIGHT)
        output_path: Where to save the mask image
    """
    pygame.init()

    # Create surface with transparency
    mask = pygame.Surface((width, height), pygame.SRCALPHA)

    # Fill with transparent black (non-walkable)
    mask.fill((0, 0, 0, 0))

    # Draw white rectangle for walkable area
    # Leave 100px margin on sides, 50px on top, 100px on bottom
    walkable_rect = pygame.Rect(100, 50, width - 200, height - 150)
    pygame.draw.rect(mask, (255, 255, 255, 255), walkable_rect)

    # Save the mask
    pygame.image.save(mask, output_path)
    print(f"✓ Created example mask: {output_path}")
    print(f"  Size: {width}x{height}")
    print(f"  Walkable area: {walkable_rect}")
    print(f"\nNow edit this file in an image editor to match your room layout!")

def create_complex_example(width=1280, height=666, output_path="example_mask_complex.png"):
    """
    Create a more complex example with obstacles.

    This creates a mask with:
    - A main walkable floor area
    - A non-walkable "table" obstacle in the center
    - Side passages
    """
    pygame.init()

    # Create surface with transparency
    mask = pygame.Surface((width, height), pygame.SRCALPHA)

    # Fill with transparent black (non-walkable)
    mask.fill((0, 0, 0, 0))

    # Draw main walkable floor
    floor_rect = pygame.Rect(100, 100, width - 200, height - 200)
    pygame.draw.rect(mask, (255, 255, 255, 255), floor_rect)

    # Cut out a "table" in the center (make it non-walkable)
    table_rect = pygame.Rect(width//2 - 100, height//2 - 75, 200, 150)
    pygame.draw.rect(mask, (0, 0, 0, 0), table_rect)

    # Add circular non-walkable "pillar" on the left
    pillar_pos = (250, height//2)
    pygame.draw.circle(mask, (0, 0, 0, 0), pillar_pos, 40)

    # Save the mask
    pygame.image.save(mask, output_path)
    print(f"✓ Created complex example mask: {output_path}")
    print(f"  Size: {width}x{height}")
    print(f"  Features: floor with table obstacle and pillar")
    print(f"\nThis demonstrates how to create areas the player cannot walk through!")

def visualize_mask(mask_path):
    """
    Simple visualization tool to preview a mask.

    Args:
        mask_path: Path to the mask image to visualize
    """
    if not os.path.exists(mask_path):
        print(f"Error: Mask file not found: {mask_path}")
        return

    pygame.init()
    mask = pygame.image.load(mask_path).convert_alpha()
    width, height = mask.get_size()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"Mask Viewer: {mask_path}")

    # Create a background to show transparency
    background = pygame.Surface((width, height))
    background.fill((50, 50, 50))

    # Draw checkerboard pattern to show transparency
    checker_size = 20
    for y in range(0, height, checker_size):
        for x in range(0, width, checker_size):
            if (x // checker_size + y // checker_size) % 2 == 0:
                pygame.draw.rect(background, (70, 70, 70),
                               (x, y, checker_size, checker_size))

    # Create green tinted version for visualization
    visualization = mask.copy()
    visualization.fill((0, 255, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)

    print(f"\nVisualizing: {mask_path}")
    print("Green areas = Walkable")
    print("Gray/Dark areas = Non-walkable")
    print("Press ESC to close")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.blit(background, (0, 0))
        screen.blit(visualization, (0, 0))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("Walkable Area Mask Generator")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "view" and len(sys.argv) > 2:
            visualize_mask(sys.argv[2])
        elif command == "create":
            output = sys.argv[2] if len(sys.argv) > 2 else "example_mask.png"
            create_example_mask(output_path=output)
        elif command == "create-complex":
            output = sys.argv[2] if len(sys.argv) > 2 else "example_mask_complex.png"
            create_complex_example(output_path=output)
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python create_example_mask.py create [output.png]")
            print("  python create_example_mask.py create-complex [output.png]")
            print("  python create_example_mask.py view <mask.png>")
    else:
        # Default: create both examples
        create_example_mask()
        create_complex_example()
        print("\n" + "=" * 60)
        print("Example masks created! Now you can:")
        print("1. View them: python create_example_mask.py view example_mask.png")
        print("2. Edit them in an image editor (Photoshop, GIMP, etc.)")
        print("3. Use them in your rooms: Room(..., walkable_mask='path/to/mask.png')")
        print("=" * 60)
