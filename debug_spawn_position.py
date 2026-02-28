#!/usr/bin/env python3
"""Check why door spawn position doesn't match."""

import pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))

# Load mask
mask = pygame.image.load('assets/rooms/TitleScreen_mask.png').convert_alpha()
mask_scaled = pygame.transform.scale(mask, (1280, 666))

# Check your defined position
defined_pos = (544, 499)
x, y = defined_pos
color = mask_scaled.get_at((x, y))
is_walkable = color.a > 128

print('='*60)
print('DOOR SPAWN POSITION DEBUG')
print('='*60)
print(f'\nYour defined position in game.py: {defined_pos}')
print(f'  Alpha value: {color.a}')
print(f'  Is walkable: {"YES" if is_walkable else "NO"}')

if not is_walkable:
    print('\n❌ Position is NOT walkable!')

    # Simulate find_nearest_walkable
    from room import Room
    from player import Player

    player = pygame.sprite.Group()
    room = Room(player, 'assets/rooms/TitleScreen.png', 'Test',
                'assets/sounds/background/Talkline7.wav',
                walkable_mask='assets/rooms/TitleScreen_mask.png')

    nearest = room.find_nearest_walkable(defined_pos)
    print(f'\nfind_nearest_walkable() returns: {nearest}')
    print('This is where main.py will place the player!')

    actual_spawn = (569, 574)
    print(f'\nYou observed player at: {actual_spawn}')

    if nearest != actual_spawn:
        print('\n⚠️  MISMATCH DETECTED!')
        print(f'Expected from find_nearest_walkable: {nearest}')
        print(f'Actual in-game: {actual_spawn}')
        print('\nPossible causes:')
        print('1. Player sprite offset is being added')
        print('2. Grid is showing player center, not spawn point')
        print('3. Player moved after spawning')

        # Check if grid shows player feet vs spawn point
        print('\nNote: Debug grid shows player FEET position')
        print('      Feet = spawn_point + player_height')
        print('\nLet me check player dimensions...')
else:
    print('\n✓ Position IS walkable!')

    actual_spawn = (569, 574)
    print(f'\nBut you see player at: {actual_spawn}')
    print('Difference:', (actual_spawn[0] - defined_pos[0], actual_spawn[1] - defined_pos[1]))

print('\n' + '='*60)
