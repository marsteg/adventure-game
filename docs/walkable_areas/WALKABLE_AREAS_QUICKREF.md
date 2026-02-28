# Walkable Areas - Quick Reference

## Basic Usage

```python
# Add walkable mask to any room:
room = Room(player, "room.png", "Room Name", "music.wav",
            walkable_mask="path/to/mask.png")
```

## Creating Masks

1. Open your room background in an image editor
2. Create a new layer
3. Paint **WHITE** where player can walk
4. Leave **TRANSPARENT/BLACK** where player cannot walk
5. Save as PNG

## Testing

- Press **W** in-game to see walkable areas (green overlay)
- Click on walls to test nearest-point finding

## Rules

- **White/Visible (alpha > 128)** = Walkable ✓
- **Black/Transparent (alpha ≤ 128)** = Blocked ✗
- No mask = Player can walk anywhere (backward compatible)

## Directory Structure

```
assets/rooms/
  ├── my_room.png
  └── masks/
      └── my_room_mask.png
```

## Helper Script

```bash
# Create example masks
python create_example_mask.py

# View a mask
python create_example_mask.py view path/to/mask.png
```

## Common Issues

**Player can't walk**: Mask is all black → paint white walkable areas
**Mask doesn't match**: Press W to visualize, check file path
**Not loading**: Check console for errors, verify PNG format

## Example

```python
tavern = Room(
    player,
    image="assets/rooms/tavern.png",
    name="Tavern",
    music="assets/sounds/background/tavern.wav",
    walkable_mask="assets/rooms/masks/tavern_mask.png"
)
```
