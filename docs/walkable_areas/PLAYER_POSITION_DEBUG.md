# Player Position Debugging Guide

## Quick Reference

Press **G** in-game to see:
- **Blue crosshair** = Player's current position (feet)
- **Top-right info box** = Player coordinates
- **Green crosshair** = Mouse position

## What You'll See

### Player Indicator (Blue)
```
         PLAYER (528, 424)
              ↓
          ────╋────  ← Blue crosshair
              │
          [player sprite]
```

### Info Boxes

**Top-Right Corner (Blue border):**
```
┌────────────────────────────┐
│ PLAYER POSITION:           │
│ Pixels: (528, 424)         │
│ Percent: (41.3%, 63.7%)    │
└────────────────────────────┘
```

**Mouse Hover (Green border):**
```
┌────────────────────────────┐
│ Position: (640, 333)       │
│ Percentage: (50.0%, 50.0%) │
│                            │
│ at_percentage_width(50.0)  │
│ at_percentage_height(50.0) │
└────────────────────────────┘
```

## Common Use Cases

### 1. Check Door Spawn Position

**Problem:** "When I enter Tourist Shop, I land in a non-walkable area"

**Solution:**
1. Press **G** to enable grid
2. Press **W** to see walkable areas (green overlay)
3. Go through the door to Tourist Shop
4. Look at the blue player indicator
5. Check if it's on green (walkable) or red (blocked)

**If player is on RED area:**
- Note the walkable position shown in the info box
- Open `game.py` and find the door definition
- Update `player_target_position` to a green area

Example:
```python
# BEFORE (spawns at non-walkable position)
shop_return = Door(..., tourist_shop, (700, 350), ...)

# AFTER (spawns at walkable position)
shop_return = Door(..., tourist_shop, (540, 500), ...)
```

### 2. Find Good Spawn Positions

**Steps:**
1. Enable grid (**G**) and walkable overlay (**W**)
2. Navigate to the target room
3. Walk your player to a good spawn location (green area, near a door)
4. Read the player's position from the top-right info box
5. Use those coordinates in your door definition

### 3. Debug "Player Gets Stuck"

**Steps:**
1. Walk player to where they get stuck
2. Press **G** to see player position
3. Press **W** to see walkable areas
4. Check if player is:
   - On a red (blocked) pixel
   - Between two walkable areas
   - Outside the mask bounds

### 4. Verify Position Changes

When you update a door spawn position:
1. Save the change in `game.py`
2. Restart the game
3. Go through the door
4. Press **G** to see where player spawned
5. Verify it matches your intended position

## Color Coding

| Color | Element | Meaning |
|-------|---------|---------|
| **Blue** | Player marker | Current player position |
| **Green** | Mouse crosshair | Where you're hovering |
| **Green** | Walkable overlay (W key) | Safe areas to walk |
| **Red** | Blocked overlay (W key) | Non-walkable areas |
| **Yellow** | % markers | Percentage grid lines |
| **Gray** | Grid lines | Coordinate reference |

## Combined Debug Views

### Grid + Walkable + Player
```
Press G - enable grid
Press W - show walkable areas

You'll see:
- Gray grid with coordinates
- Green/red walkable overlay
- Blue player position marker
- Mouse position (green) when hovering
```

Perfect for finding good spawn positions!

### Grid + Interactive Objects + Player
```
Press G - enable grid
Press SPACE - highlight objects

You'll see:
- Object positions and hitboxes
- Player position relative to objects
- Distance between player and objects
```

Perfect for checking if player can reach objects!

## Troubleshooting Door Spawns

### Issue: "Player spawns outside walkable area"

**Diagnosis:**
1. Press **G + W** when entering room
2. Look at blue player marker
3. Is it on red (blocked) area?

**Fix:**
```python
# In game.py, find the door leading to this room
# Example: shop_return door
shop_return = Door(
    50, 350, 80, 120,
    "assets/doors/door1.png",
    "Shop Return",
    tourist_shop,
    (528, 424),  # ← OLD: Non-walkable position
    False, None
)

# Update to walkable position (use grid to find it)
shop_return = Door(
    50, 350, 80, 120,
    "assets/doors/door1.png",
    "Shop Return",
    tourist_shop,
    (540, 500),  # ← NEW: Walkable position
    False, None
)
```

### Issue: "Position not updating after code change"

**Checklist:**
- ✓ Did you save `game.py`?
- ✓ Did you restart the game (changes don't apply mid-game)?
- ✓ Are you testing the right door?
- ✓ Is the position actually walkable? (check with **W** key)

### Issue: "Player spawns somewhere different than I specified"

**Cause:** The `find_nearest_walkable()` function is overriding your position because it's not walkable!

**Check:**
```bash
# Test if your position is walkable
python -c "
import pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
from room import Room
from player import Player

player = pygame.sprite.Group()
room = Room(player, 'assets/rooms/TitleScreen.png', 'Test',
            'assets/sounds/background/Talkline7.wav',
            walkable_mask='assets/rooms/TitleScreen_mask.png')

# Test your position
pos = (528, 424)  # ← Your door spawn position
is_walkable = room.is_walkable(pos)
print(f'Position {pos} is walkable: {is_walkable}')

if not is_walkable:
    nearest = room.find_nearest_walkable(pos)
    print(f'Nearest walkable: {nearest}')
    print('Player will spawn HERE instead!')
"
```

## Tips

1. **Always test door spawns** after creating/modifying doors
2. **Use walkable overlay** when finding spawn positions
3. **Player feet position** is what matters for collision (center-bottom)
4. **Percentage-based positioning** is more maintainable than pixels
5. **Keep spawn positions** away from room edges (at least 50px in)

## Example Workflow: Fix Door Spawn

```bash
# 1. Identify the problem
Run game → Go through door → Player stuck in wall

# 2. Debug with grid
Press G → Press W → See player on RED area

# 3. Find good position
Walk around → Find green (walkable) area near door
Note position from blue info box: (540, 500)

# 4. Update code
Edit game.py → Find door definition
Change player_target_position to (540, 500)

# 5. Verify
Restart game → Go through door
Press G → Verify player is on GREEN area ✓
```

---

**Feature:** Player position indicator in debug grid
**Commit:** 9ac0b3d
