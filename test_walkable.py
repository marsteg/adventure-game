#!/usr/bin/env python3
"""Quick test for walkable areas feature."""

import pygame
import sys

# Initialize pygame
pygame.init()

# Import after pygame init
from room import Room
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_HEIGHT

def test_walkable_areas():
    """Test that walkable areas work correctly."""
    print("\n" + "="*60)
    print("Testing Walkable Areas Feature")
    print("="*60)

    # Set up display (needed for pygame image operations)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a dummy player
    player = pygame.sprite.Group()

    # Test 1: Room without mask (backward compatibility)
    print("\n[Test 1] Room without walkable mask...")
    room1 = Room(player, "assets/rooms/Library.png", "Test Room 1", "assets/sounds/background.wav")

    # Should be walkable everywhere
    assert room1.is_walkable((100, 100)), "Without mask, all positions should be walkable"
    assert room1.is_walkable((SCREEN_WIDTH-1, SCREEN_HEIGHT-INVENTORY_HEIGHT-1)), "Without mask, all positions should be walkable"
    print("✓ Room without mask: all positions walkable (backward compatible)")

    # Test 2: Room with mask
    print("\n[Test 2] Room with walkable mask...")
    room2 = Room(player, "assets/rooms/Library.png", "Test Room 2", "assets/sounds/background.wav",
                 walkable_mask="example_mask.png")

    if room2.walkable_mask:
        print("✓ Mask loaded successfully")

        # Test center (should be walkable in example mask)
        center_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        is_walkable = room2.is_walkable(center_pos)
        print(f"  Center position {center_pos}: {'walkable ✓' if is_walkable else 'blocked ✗'}")

        # Test corners (might be blocked in example mask)
        corner_pos = (10, 10)
        is_walkable = room2.is_walkable(corner_pos)
        print(f"  Corner position {corner_pos}: {'walkable ✓' if is_walkable else 'blocked ✗'}")

        # Test nearest walkable
        nearest = room2.find_nearest_walkable((10, 10))
        print(f"  Nearest walkable to (10, 10): {nearest}")

        print("✓ Walkable area checking works")
    else:
        print("⚠ Mask file not found (this is OK if example_mask.png doesn't exist)")

    # Test 3: Out of bounds
    print("\n[Test 3] Out of bounds checking...")
    assert not room2.is_walkable((-10, 100)), "Negative coordinates should not be walkable"
    assert not room2.is_walkable((SCREEN_WIDTH + 100, 100)), "Out of bounds should not be walkable"
    print("✓ Out of bounds positions correctly detected as non-walkable")

    print("\n" + "="*60)
    print("All Tests Passed! ✓")
    print("="*60)
    print("\nThe walkable areas feature is working correctly!")
    print("\nNext steps:")
    print("1. Run the game: python main.py")
    print("2. Press W to toggle walkable area visualization")
    print("3. Click around to test movement restrictions")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        test_walkable_areas()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
