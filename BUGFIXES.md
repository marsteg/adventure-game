# Walkable Areas Bug Fixes

## Issues Found and Fixed

### 1. **Player Walking Through Walls (CRITICAL)**

**Problem**: The player was only checking if the **final target position** was walkable, but not validating **each step** along the path.

**Example**:
```
Player at (100, 100) clicks on (900, 100)
Target is walkable ✓
But path goes through a wall at (500, 100) ✗
Player walks straight through the wall!
```

**Fix**: Modified `player.py` to validate each movement increment:
- Changed `update(dt)` to `update(dt, room=None)`
- Now checks the player's "feet" position (center-bottom) every frame
- Stops movement immediately when hitting a non-walkable pixel
- Uses: `room.is_walkable((feet_x, feet_y))` before each movement

**Result**: Player now stops when hitting walls instead of passing through them.

---

### 2. **Direct Position Assignments Bypassing Validation**

**Problem**: Several places in the code set player position directly without checking walkability:

#### Fixed in `main.py`:

**a) Starting Position (line 122-123)**
```python
# BEFORE (bypassed walkable check):
daisy.pos = pygame.Vector2(start_x, start_y)

# AFTER (validates position):
start_pos = pygame.Vector2(start_x, start_y)
walkable_start = active_room.find_nearest_walkable(start_pos)
daisy.pos = pygame.Vector2(walkable_start)
```

**b) Door Transitions (line 268)**
```python
# BEFORE:
daisy.pos = pygame.Vector2(obj.player_target_position)

# AFTER:
target_pos = pygame.Vector2(obj.player_target_position)
walkable_pos = active_room.find_nearest_walkable(target_pos)
daisy.pos = pygame.Vector2(walkable_pos)
```

**c) Loading Saved Games (line 208)**
```python
# BEFORE:
player.sprites()[0].pos = pygame.Vector2(player_x, player_y)

# AFTER:
loaded_pos = pygame.Vector2(player_x, player_y)
walkable_pos = active_room.find_nearest_walkable(loaded_pos)
player.sprites()[0].pos = walkable_pos
```

---

### 3. **Player Update Not Receiving Room Context**

**Problem**: Player's update method had no way to check walkability because it didn't know which room it was in.

**Fix in `main.py` (line 897)**:
```python
# BEFORE:
player.update(dt)

# AFTER:
for char in player.sprites():
    char.update(dt, active_room)  # Now passes room for validation
```

---

## New Tools Added

### `visualize_mask.py` - Mask Debugging Tool

**Usage**:
```bash
python visualize_mask.py assets/rooms/TitleScreen_mask.png
```

**Features**:
- Shows GREEN for walkable areas (alpha > 128)
- Shows RED for blocked areas (alpha ≤ 128)
- Displays pixel info on mouse hover
- Press SPACE to toggle overlay
- Analyzes mask statistics (% walkable vs blocked)

**Warnings it detects**:
- Less than 10% walkable (mask might be inverted)
- More than 90% walkable (no obstacles defined)

---

## How It Works Now

### Movement Flow:
1. **Player clicks** position (x, y)
2. `main.py` calls `active_room.find_nearest_walkable((x, y))`
3. If clicked position is blocked, spiral search finds nearest walkable point
4. Player's `set_target()` is called with walkable position
5. **Every frame** in `player.update()`:
   - Calculate next position (current + direction × speed)
   - Check if new "feet" position is walkable
   - If YES: move there
   - If NO: stop moving (hit a wall)

### Collision Detection Point:
```python
# Check the center-bottom of player sprite (their "feet")
feet_x = int(new_pos.x + self.rect.width // 2)
feet_y = int(new_pos.y + self.rect.height)
```

This ensures the player's feet stay on walkable ground, not their head or center.

---

## Testing Your Mask

Your `TitleScreen_mask.png` analysis:
- Original size: 1024×1024
- Scaled to: 1280×666
- **Only 3% walkable!** (11 walkable samples out of 364)

### Recommendations:

1. **Check if your mask is inverted**:
   - Should be: WHITE/OPAQUE = walkable, BLACK/TRANSPARENT = blocked
   - Your mask appears to be mostly blocked

2. **Use the visualization tool**:
   ```bash
   python visualize_mask.py assets/rooms/TitleScreen_mask.png
   ```
   This will show you exactly where players can walk (green) and can't walk (red)

3. **Fix your mask**:
   - Open in image editor (Photoshop, GIMP, etc.)
   - Paint WHITE with full opacity on floor areas
   - Paint BLACK or transparent on walls/obstacles
   - Save as PNG with alpha channel

4. **Recommended workflow**:
   ```bash
   # Edit mask in image editor
   # Then visualize it
   python visualize_mask.py assets/rooms/TitleScreen_mask.png
   # Test in game
   python main.py
   # Press W to see overlay in-game
   ```

---

## Mask Creation Tips

### Good Mask:
```
- Floor areas: WHITE, alpha = 255
- Walls/furniture: BLACK, alpha = 0
- 30-70% walkable area (typical)
- Matches room layout exactly
```

### Common Issues:

**Issue**: "Player can walk anywhere"
- Mask is all white/opaque
- No obstacles defined

**Issue**: "Player can't walk anywhere"  ← **YOUR CURRENT ISSUE**
- Mask is all black/transparent
- Mask might be inverted
- Check alpha channel values

**Issue**: "Player walks through some walls"
- Mask doesn't align with room image
- Scaling issues (use same dimensions)
- Some areas not painted blocked

**Issue**: "Player gets stuck"
- Walkable areas too narrow
- No path between areas
- Use spiral search radius increase if needed

---

## Testing Checklist

After these fixes, test:
- ✅ Click on floor - player walks there
- ✅ Click on wall - player walks to nearest floor
- ✅ Walk towards wall - player stops at wall
- ✅ Walk along wall - player follows wall edge
- ✅ Enter door - player spawns in valid position
- ✅ Load save - player loads in valid position
- ✅ Press W - see green overlay on walkable areas

---

## Summary

The main bug was **player validates target, but not path**. Now fixed with per-frame collision detection.

Your specific issue is likely **your mask is 97% blocked** - use the visualization tool to verify and fix the mask.

**Next steps**:
1. Run: `python visualize_mask.py assets/rooms/TitleScreen_mask.png`
2. Fix the mask in an image editor if needed
3. Test in game with W key to see overlay
4. Report if issues persist

---

**Commit**: 4913826 - "Fix walkable areas collision detection bugs"
