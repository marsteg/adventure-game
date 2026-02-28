# Walkable Areas - Complete Guide

## Overview

The walkable area system allows you to restrict where the player can walk in each room using an image mask. This is essential for creating realistic environments where the player shouldn't walk through walls, over furniture, or into other obstacles.

## How It Works

The system uses a **mask image** (like a stencil) where:
- **White/Visible pixels** = Player CAN walk here
- **Black/Transparent pixels** = Player CANNOT walk here

When a player clicks on a non-walkable area, the system automatically finds the nearest walkable point.

---

## Step-by-Step Tutorial

### Step 1: Create Your Room Background

First, create your room background image as usual (e.g., `my_room.png`).

### Step 2: Create the Walkable Mask Image

#### Option A: Using Photoshop/GIMP (Recommended)

1. **Open your room background** in your image editor
2. **Create a new layer** on top
3. **Paint white** where the player can walk (floor areas, paths, etc.)
4. **Leave transparent/black** where the player cannot walk (walls, furniture, obstacles)
5. **Save only the mask layer** as `my_room_mask.png` (PNG with transparency)

**Tips:**
- Use a white brush to "paint" walkable areas
- Lower opacity to see the background while painting
- Be generous with floor areas - it's better to have slightly too much walkable space than too little
- Save the mask at the same resolution as your room image (will be scaled automatically)

#### Option B: Quick Method with Paint/Preview

1. **Copy your room image**
2. **Use a white brush/pencil** to cover walkable floor areas
3. **Use a black brush/eraser** for non-walkable areas
4. **Save as PNG** with name like `my_room_mask.png`

### Step 3: Add Mask to Room in Code

In your `game.py` file, add the mask when creating a room:

```python
# WITHOUT walkable mask (old way - player can walk anywhere)
my_room = Room(player, "assets/rooms/my_room.png", "My Room", "music.wav")

# WITH walkable mask (new way - player restricted to mask)
my_room = Room(player,
               "assets/rooms/my_room.png",
               "My Room",
               "music.wav",
               walkable_mask="assets/rooms/masks/my_room_mask.png")
```

**That's it!** The system handles everything else automatically.

---

## Directory Structure

Recommended folder structure:

```
assets/
├── rooms/
│   ├── my_room.png          # Room background
│   ├── another_room.png
│   └── masks/               # Walkable masks subfolder
│       ├── my_room_mask.png
│       └── another_room_mask.png
```

---

## Testing & Debugging

### Visualizing the Walkable Area

Press **W** during gameplay to toggle the walkable area overlay:
- **Green overlay** = walkable areas
- **No overlay** = blocked areas

This helps you fine-tune your mask images.

### Testing Checklist

1. ✓ Load your room and press **W** to see the walkable area
2. ✓ Try clicking various spots - does the player move correctly?
3. ✓ Click on walls/obstacles - does the player find the nearest walkable point?
4. ✓ Walk near edges - does the player stay inside the walkable area?

---

## Advanced Features

### Automatic Nearest Point Finding

If a player clicks on a non-walkable area (like a wall), the system searches in a spiral pattern up to 200 pixels away to find the nearest walkable point. The player will walk there instead.

**Example:**
- Player clicks on a table (non-walkable)
- System finds the floor next to the table (walkable)
- Player walks to the floor beside the table

### Backward Compatibility

Rooms without a `walkable_mask` parameter work exactly as before - the player can walk anywhere. This means:
- You can add masks gradually to your game
- Old rooms continue to work without changes
- No need to update all rooms at once

---

## Common Issues & Solutions

### Issue: Player can't walk anywhere
**Solution:** Your mask is probably all black/transparent. Make sure walkable areas are **white** or have high opacity (alpha > 128).

### Issue: Mask doesn't match room layout
**Solution:**
1. Press **W** to visualize the mask
2. Check that your mask image matches your room dimensions
3. Verify you're editing the correct mask file

### Issue: Player gets stuck near edges
**Solution:**
- Make your walkable areas slightly larger
- Use softer edges in your mask (but keep alpha > 128 for walkable areas)

### Issue: Walkable mask not loading
**Solution:**
- Check the file path is correct
- Ensure the mask image is PNG format
- Look at console for error messages (the system will print warnings)

---

## Example: Complete Room Setup

Here's a complete example showing how to set up a room with a walkable area:

```python
# In game.py

# Create the room with walkable mask
tavern = Room(
    player,
    image="assets/rooms/tavern.png",
    name="Tavern",
    music="assets/sounds/background/tavern_music.wav",
    walkable_mask="assets/rooms/masks/tavern_mask.png"  # <- Add this parameter
)

# Add objects to room as usual
tavern.npcs[bartender.name] = bartender
tavern.items[key.name] = key
tavern.doors[exit_door.name] = exit_door
```

---

## Keyboard Shortcuts Reference

| Key | Function |
|-----|----------|
| **W** | Toggle walkable area visualization (green overlay) |
| **SPACE** | Show all interactive objects |
| **S** | Save game |
| **L** | Load game |
| **ESC** | Return to menu |

---

## Performance Notes

- Mask images are automatically cached - no performance penalty
- Mask checking is very fast (O(1) pixel lookup)
- The nearest-point search only runs when clicking non-walkable areas
- Mask images can be any size - they're scaled to match screen resolution

---

## Tips for Game Designers

1. **Start Simple**: Create basic rectangular walkable areas first, then refine
2. **Be Generous**: Give players more space than less - walking near walls looks fine
3. **Test Early**: Add masks to rooms as you create them, not at the end
4. **Visual Consistency**: Use the W key frequently to ensure mask matches room visually
5. **Reuse Masks**: Rooms with similar layouts can share mask images

---

## Technical Details

### How Pixel Detection Works

The system checks the alpha channel of the mask image:
- **Alpha > 128** = Walkable (pixel is visible)
- **Alpha ≤ 128** = Non-walkable (pixel is transparent/dark)

This means you can use:
- White pixels (255, 255, 255, 255) ✓
- Any bright color with high alpha ✓
- Transparent pixels (any color with alpha < 128) ✗
- Black pixels (0, 0, 0, 255) if you want (depends on alpha)

### Interaction System Integration

When a player queues an interaction (clicks on an NPC, door, item, etc.):
1. System calculates the center point of the object
2. Finds the nearest walkable point to that center
3. Player walks to the walkable point
4. Interaction executes when player reaches it

This ensures players always walk to valid positions before interacting with objects.

---

## Examples Gallery

### Example 1: Simple Room with Floor Area
```
Room: Simple bedroom
Walkable: Central floor area only
Blocked: Walls, bed, dresser
```

### Example 2: Complex Room with Paths
```
Room: Castle hallway with pillars
Walkable: Paths between pillars, main corridor
Blocked: Pillars, walls, decorative statues
```

### Example 3: Outdoor Scene
```
Room: Forest path
Walkable: Dirt path, clearings
Blocked: Trees, bushes, water
```

---

## Future Enhancements

Potential future features (not yet implemented):
- Multiple walkable zones per room
- Dynamic walkable areas (areas that open/close during gameplay)
- Height-based walking (stairs, elevation)
- Visual editor for creating masks

---

## Questions?

If you encounter issues or have questions:
1. Check the console output for error messages
2. Use the W key to visualize your walkable areas
3. Verify your mask image paths are correct
4. Ensure mask images are PNG format with transparency

Remember: Rooms without masks work normally, so you can always remove the `walkable_mask` parameter if something isn't working and debug later!
