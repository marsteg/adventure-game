# Spawn Point vs Feet Position - Visual Guide

## What You'll See Now

When you press **G** in-game, you'll see TWO markers for the player:

```
    SPAWN (544, 499) ← Cyan square (top-left of sprite)
        ┌─────────┐
        │         │
        │ Player  │  50px wide
        │ Sprite  │  75px tall
        │         │
        └────┬────┘
             │
        FEET (569, 574) ← Blue circle (center-bottom)
```

## Color Coding

| Marker | Color | Position | What It Means |
|--------|-------|----------|---------------|
| **Square** | Cyan | Top-left | Door spawn position (`player_target_position`) |
| **Circle** | Blue | Center-bottom | Collision/walkability check point |
| **Line** | Light blue | Connects both | Visual relationship |

## Understanding the Offset

For a player sprite of **50×75 pixels**:

```
Spawn point (top-left):    (544, 499)
                              ↓
Add width/2:               +25
Add height:                      +75
                              ↓
Feet position:             (569, 574)
```

**Formula:**
- `feet_x = spawn_x + width/2`
- `feet_y = spawn_y + height`

## Info Box (Top-Right)

```
┌────────────────────────────┐
│ PLAYER POSITION:           │
│ Spawn: (544, 499)          │ ← Cyan (use in doors)
│        (42.5%, 74.9%)      │
│ Feet:  (569, 574)          │ ← Blue (walkability)
│        (44.5%, 86.2%)      │
└────────────────────────────┘
```

## Which Position to Use?

### For Door Definitions (game.py)
Use the **CYAN SPAWN** position:

```python
shop_return = Door(
    50, 350, 80, 120,
    "assets/doors/door1.png",
    "Shop Return",
    tourist_shop,
    (544, 499),  # ← Use SPAWN position (cyan square)
    False, None
)
```

### For Walkability Checks
The **BLUE FEET** position is automatically used by the collision system.

## Why This Matters

### Problem You Encountered:
- You set door spawn to: `(544, 499)` ✓
- Grid showed player at: `(569, 574)`
- You thought it was a bug ✗

### Reality:
Both are correct! Just different reference points:
- `(544, 499)` = where sprite starts (top-left)
- `(569, 574)` = where feet touch ground (walkability)

## Practical Examples

### Example 1: Positioning a Door Spawn

**Goal:** Player should spawn in the center of a room

1. Press **G** in the room
2. Walk player to desired position
3. **Read the CYAN spawn position** from info box
4. Use that in your door definition

```python
# Info box shows:
# Spawn: (640, 450)

# Use in door:
my_door = Door(..., target_room, (640, 450), ...)
```

### Example 2: Checking Walkability

**Goal:** Verify player spawns on walkable area

1. Press **G + W** (grid + walkable overlay)
2. Go through door
3. **Check the BLUE feet marker**
4. Is it on GREEN (walkable)? ✓
5. If on RED (blocked), adjust spawn position

### Example 3: Understanding "Off by 25, 75"

**Question:** Why doesn't my (500, 400) spawn show at (500, 400)?

**Answer:**
```
You set spawn:    (500, 400) ← Top-left of sprite
Grid shows feet:  (525, 475) ← Center-bottom
Offset:           (+25, +75) ← Player dimensions (50×75)
```

This is **correct behavior**, not a bug!

## Visual Reference

### Player Sprite Breakdown
```
        SPAWN (x, y) ← Door sets this
        ↓
        ┌──────────┐  ← Top of sprite
        │          │
        │  50px    │  Width
        │          │
        │   75px   │  Height
        │          │
        └─────┬────┘  ← Bottom of sprite
              ↓
         FEET (x+25, y+75) ← Collision checks this
```

### On Grid
```
         Grid shows both:

    ▢ ← Cyan spawn marker (square)
    │   Light blue connecting line
    ●   ← Blue feet marker (circle)
```

## Common Questions

### Q: Which position should I write in my code?
**A:** The **cyan spawn position**. The feet position is calculated automatically.

### Q: Why is the spawn position not on the ground?
**A:** It's the top-left of the sprite. The feet (at the bottom) are what touch the ground.

### Q: How do I know if my spawn is walkable?
**A:** Check if the **blue feet marker** is on green when using the walkable overlay (W key).

### Q: The feet marker is in a wall! Is that a bug?
**A:** No, adjust your **spawn position** upward/leftward so the feet land on walkable area.

### Q: Can I make the spawn equal to feet?
**A:** No, they're different by design. Spawn is top-left, feet is bottom-center.

## Testing Workflow

### Complete Door Spawn Test:
```
1. Press G (enable grid)
2. Press W (show walkable areas)
3. Go through door
4. Check cyan spawn square - matches your code? ✓
5. Check blue feet circle - on green area? ✓
6. If feet on red, adjust spawn position
7. Update door in game.py
8. Restart and retest
```

## Debug Commands

### See spawn for current position:
```python
# In Python console or debug script:
player_feet = (569, 574)  # From grid
player_width = 50
player_height = 75

spawn_x = player_feet[0] - player_width // 2
spawn_y = player_feet[1] - player_height

print(f"Spawn position: ({spawn_x}, {spawn_y})")
# Output: Spawn position: (544, 499)
```

### Calculate feet from spawn:
```python
spawn = (544, 499)  # Your door position
player_width = 50
player_height = 75

feet_x = spawn[0] + player_width // 2
feet_y = spawn[1] + player_height

print(f"Feet position: ({feet_x}, {feet_y})")
# Output: Feet position: (569, 574)
```

---

**Now you can see both positions and understand exactly where your player is!**

**Commit:** 0fdb6f4
