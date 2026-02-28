# Walkable Areas System - Agent Guide Addition

*This content should be inserted after the "Room Creation Pattern" section in Agent.md*

---

## Walkable Areas System

### Overview

The walkable areas system allows you to restrict player movement using image masks. This prevents players from walking through walls, furniture, or other obstacles, creating more realistic and polished gameplay.

**Key Features:**
- Mask-based collision detection (PNG images)
- Per-frame movement validation
- Smart pathfinding to nearest walkable point
- Debug visualization tools
- **Optional and backward compatible** - existing rooms work without masks

### When to Use Walkable Areas

**Use walkable masks when:**
- Rooms have walls, furniture, or obstacles that should block movement
- You want realistic collision detection
- The room layout has clear floor vs non-floor areas
- You want to guide player movement naturally

**Skip walkable masks when:**
- The entire room is open space (no obstacles)
- You want complete freedom of movement
- Room is abstract or doesn't need collision

### Creating Walkable Area Masks

#### Understanding Mask Images

A walkable mask is a PNG image with alpha transparency where:
- **WHITE/OPAQUE pixels (alpha > 128)** = Walkable areas (floors, paths)
- **BLACK/TRANSPARENT pixels (alpha ≤ 128)** = Blocked areas (walls, obstacles)

**Visual Example:**
```
Room Background:          Walkable Mask:
┌─────────────┐          ┌─────────────┐
│ ╔═══════╗   │          │ ░░░░░░░░░   │  ← Walls (black/transparent)
│ ║ Table ║   │          │ ░░░░░░░░░   │
│ ╚═══════╝   │          │ ░░░░░░░░░   │
│             │    →     │ ▓▓▓▓▓▓▓▓▓▓▓ │  ← Floor (white/opaque)
│   Player→   │          │ ▓▓▓▓▓▓▓▓▓▓▓ │
│   Floor     │          │ ▓▓▓▓▓▓▓▓▓▓▓ │
└─────────────┘          └─────────────┘
```

#### Method 1: Image Editor (Recommended)

Use Photoshop, GIMP, Krita, or similar:

1. **Open room background** in your image editor
2. **Create new layer** above the background
3. **Paint WHITE** on areas where player can walk (floors, paths)
4. **Leave BLACK/TRANSPARENT** where player cannot walk (walls, furniture)
5. **Export only the mask layer** as PNG with transparency
6. **Save to**: `assets/rooms/masks/roomname_mask.png`

**Tips:**
- Match the room's dimensions or use any size (auto-scaled to 1280×666)
- Use solid white (255, 255, 255, alpha 255) for walkable areas
- Use solid black (0, 0, 0, alpha 0) or transparent for blocked areas
- Test with the visualization tool (see below)

#### Method 2: Helper Script

Generate example masks to understand the format:

```bash
# Generate example masks
python create_example_mask.py

# View the generated masks
python visualize_mask.py example_mask.png
python visualize_mask.py example_mask_complex.png
```

These examples show:
- `example_mask.png` - Simple rectangular walkable area
- `example_mask_complex.png` - Complex layout with obstacles

#### Method 3: Paint Tool Workflow

For simple masks using any paint program:

1. **Create new image** (any size, will be auto-scaled)
2. **Fill with BLACK** (blocked by default)
3. **Use WHITE brush** to paint walkable floor areas
4. **Save as PNG** with transparency support
5. **Test in game** with debug overlays

### Implementing Walkable Areas

#### Adding Mask to Room

```python
# Room without walkable areas (legacy, all areas walkable)
room1 = Room(player, "assets/rooms/library.png", "Library",
             "assets/sounds/background.wav")

# Room with walkable areas (recommended for realistic collision)
room2 = Room(player, "assets/rooms/library.png", "Library",
             "assets/sounds/background.wav",
             walkable_mask="assets/rooms/masks/library_mask.png")
```

**That's it!** The engine automatically:
- Loads and caches the mask image
- Validates player movement every frame
- Finds nearest walkable points when clicking blocked areas
- Ensures door spawns place player in valid positions

#### Door Spawn Positions with Walkable Areas

When using walkable masks, door spawn positions must place the player's **feet** on walkable areas:

```python
# IMPORTANT: Spawn position is top-left of player sprite
# Player is 50×75 pixels, so feet are at (spawn_x + 25, spawn_y + 75)

# Create door with valid spawn position
door = Door(
    50, 350, 80, 120,
    "assets/doors/door1.png",
    "Exit",
    target_room,
    (500, 450),  # Spawn position where player's feet will be walkable
    False, None
)
```

**Critical Understanding:**
- Door `player_target_position` = **top-left corner** of player sprite
- Player **feet** (collision point) = `(spawn_x + 25, spawn_y + 75)`
- Engine validates that **feet position** is walkable, not spawn position
- Use debug grid (G key) to find valid spawn positions (see below)

### Debug Tools for Walkable Areas

The engine includes powerful debug tools to help you create and test walkable areas:

#### 1. Walkable Overlay (W Key)

Press **W** during gameplay to toggle visualization:
- **GREEN overlay** = Walkable areas (player can walk here)
- **RED overlay** = Blocked areas (walls, obstacles)

**Usage:**
1. Run game: `python main.py`
2. Navigate to room with walkable mask
3. Press **W** to see overlay
4. Verify green areas match your intended floor space

#### 2. Debug Grid (G Key)

Press **G** during gameplay for positioning tools:

**Features:**
- Coordinate grid (50px fine, 100px major lines)
- Percentage markers (for `at_percentage_width/height()`)
- Mouse position info box
- **Spawn calculator** - hover mouse to see required spawn position
- **Player position display** - shows spawn (cyan) and feet (blue) markers

**Finding Valid Door Spawn Positions:**

```
1. Press G (enable grid)
2. Press W (show walkable overlay)
3. Navigate to target room
4. Hover mouse over GREEN walkable area where you want player feet
5. Read from info box: "Spawn if feet here: (500, 450)"
6. Use that position in your door definition ✓
```

**Example Info Box:**
```
┌────────────────────────────────────┐
│ Mouse (Feet): (525, 525)           │ ← Where you're hovering
│ Percentage: (41.0%, 78.9%)         │
│                                    │
│ Spawn if feet here: (500, 450)    │ ← USE THIS! (cyan text)
│ Percentage: (39.1%, 67.7%)         │
│                                    │
│ at_percentage_width(39.1)          │ ← Copy-paste ready
│ at_percentage_height(67.7)         │
└────────────────────────────────────┘
```

#### 3. Mask Visualization Tool

Visualize mask files before using them in game:

```bash
# View any mask file
python visualize_mask.py assets/rooms/masks/library_mask.png

# Features:
# - Shows walkable (green) vs blocked (red) areas
# - Hover mouse to see pixel alpha values
# - Press SPACE to toggle overlay on/off
# - Verify mask before implementing
```

### Walkable Areas Workflow

**Complete workflow for adding walkable areas to a room:**

#### Step 1: Create Room Background
```python
# Create your room art (backgrounds, furniture, etc.)
# Example: library.png with bookshelves, tables, chairs
```

#### Step 2: Create Walkable Mask
```python
# Option A: Image editor
# 1. Open library.png
# 2. Create new layer
# 3. Paint white on floor areas (between furniture)
# 4. Export layer as library_mask.png

# Option B: Use helper script to understand format
python create_example_mask.py
# Study the examples, then create your own
```

#### Step 3: Visualize and Test Mask
```bash
# View your mask
python visualize_mask.py assets/rooms/masks/library_mask.png

# Check:
# - Floor areas are GREEN ✓
# - Walls/furniture are RED ✓
# - No gaps in walkable areas
# - Reasonable coverage (30-70% walkable typical)
```

#### Step 4: Add Mask to Room
```python
library = Room(
    player,
    "assets/rooms/library.png",
    "Library",
    "assets/sounds/background/library_music.wav",
    walkable_mask="assets/rooms/masks/library_mask.png"  # Add this line
)
```

#### Step 5: Find Door Spawn Positions
```bash
# In game:
# 1. Press G + W (grid + walkable overlay)
# 2. Hover mouse on GREEN area near entrance
# 3. Note "Spawn if feet here" position from info box
# 4. Use in door definitions
```

#### Step 6: Test in Game
```bash
# Run game
python main.py

# Test:
# - Click on floor (player walks there) ✓
# - Click on walls (player walks to nearest floor) ✓
# - Walk around (player stops at obstacles) ✓
# - Use doors (player spawns in valid position) ✓
```

### Common Patterns and Examples

#### Pattern 1: Room with Furniture
```python
# Living room with couch, table, TV stand
living_room = Room(
    player,
    "assets/rooms/living_room.png",
    "Living Room",
    "assets/sounds/background/home_ambient.wav",
    walkable_mask="assets/rooms/masks/living_room_mask.png"
)

# Mask: White floor in center and around furniture, black for furniture outlines
```

#### Pattern 2: Outdoor Scene with Paths
```python
# Garden with paths, trees, bushes
garden = Room(
    player,
    "assets/rooms/garden.png",
    "Garden",
    "assets/sounds/background/birds.wav",
    walkable_mask="assets/rooms/masks/garden_mask.png"
)

# Mask: White paths and clearings, black for trees/bushes/water
```

#### Pattern 3: Complex Indoor Layout
```python
# Office with desks, filing cabinets, doorways
office = Room(
    player,
    "assets/rooms/office.png",
    "Office",
    "assets/sounds/background/office_ambient.wav",
    walkable_mask="assets/rooms/masks/office_mask.png"
)

# Mask: White narrow paths between furniture, black for desks/cabinets
```

#### Pattern 4: Open Room (No Mask Needed)
```python
# Empty warehouse - all areas walkable
warehouse = Room(
    player,
    "assets/rooms/warehouse.png",
    "Warehouse",
    "assets/sounds/background/warehouse.wav"
    # No walkable_mask - entire room is walkable
)
```

### Technical Details

#### How It Works

1. **Mask Loading**: PNG loaded and scaled to 1280×666 (playable area)
2. **Per-Frame Check**: Every movement, player's feet position checked
3. **Alpha Threshold**: Pixels with alpha > 128 considered walkable
4. **Collision Response**: Movement stops when hitting non-walkable pixel
5. **Smart Pathfinding**: Clicks on blocked areas find nearest walkable point

#### Player Dimensions
- **Width**: 50 pixels
- **Height**: 75 pixels
- **Feet Position**: `(spawn_x + 25, spawn_y + 75)`
- **Collision Point**: Center-bottom of sprite (feet)

#### Performance
- **Image Caching**: Masks loaded once, cached for entire session
- **O(1) Checks**: Single pixel lookup per frame
- **Optimized Search**: Spiral search only when needed, max 200px radius
- **Minimal Overhead**: ~1-2% performance impact

#### Mask Format Requirements
- **File Format**: PNG with alpha channel
- **Recommended Size**: Match room dimensions or use any size (auto-scaled)
- **Color Space**: RGB or RGBA
- **Walkable**: Alpha > 128 (white/opaque)
- **Blocked**: Alpha ≤ 128 (black/transparent)

### Troubleshooting Walkable Areas

#### Issue: "Player can walk anywhere"
**Cause**: Mask is all white/opaque
**Fix**: Paint obstacles black/transparent in your mask

#### Issue: "Player can't walk anywhere"
**Cause**: Mask is all black/transparent
**Fix**: Paint floor areas white/opaque in your mask

#### Issue: "Player spawns in wall after door transition"
**Cause**: Door spawn position not walkable
**Solution**:
```python
# Use debug grid to find valid position:
# 1. Press G + W in target room
# 2. Hover on GREEN area
# 3. Copy "Spawn if feet here" value
# 4. Update door:
door.player_target_position = (500, 450)  # From grid
```

#### Issue: "Mask doesn't align with room"
**Cause**: Mask dimensions don't match or incorrect walkable areas
**Fix**:
1. Visualize mask: `python visualize_mask.py mask.png`
2. Overlay in game: Press W to compare
3. Edit mask in image editor to match room layout

#### Issue: "Player walks through some walls"
**Cause**: Gaps in blocked areas of mask
**Fix**:
1. Visualize mask to find gaps
2. Fill gaps with black in image editor
3. Test with W key overlay

#### Issue: "Walkable area too small"
**Cause**: Too much of mask is blocked
**Recommendations**:
- 30-70% walkable area is typical
- Leave enough room for player movement
- Path width should be > 100px for comfort

### Best Practices for Walkable Areas

#### Design Guidelines
1. **Match Art Style**: Walkable areas should align with visual floor space
2. **Generous Paths**: Make walkable paths wider than strictly necessary
3. **Natural Flow**: Guide players through rooms with clear pathways
4. **Test Early**: Add masks early in development, not as afterthought
5. **Consistent Coverage**: Similar room types should have similar walkable ratios

#### Mask Creation Tips
1. **Start with Background**: Use room image as reference layer
2. **Paint Generously**: Slightly larger walkable areas feel better
3. **Round Corners**: Smooth walkable area edges for natural movement
4. **Test Iteratively**: Make mask → test → adjust → repeat
5. **Document Paths**: Keep notes on intended player paths through rooms

#### Door Positioning
1. **Always Use Grid**: Press G to find exact spawn positions
2. **Test Both Directions**: Verify door works entering AND exiting
3. **Near Edges**: Place spawns 50-100px from room edges
4. **Near Doors**: Spawn players near door location but in open space
5. **Validate in Game**: Always test door transitions with W overlay

### Debug Controls Reference

| Key | Function | Usage |
|-----|----------|-------|
| **G** | Toggle Debug Grid | Shows coordinate grid, spawn calculator, player position |
| **W** | Toggle Walkable Overlay | Shows green (walkable) and red (blocked) areas |
| **SPACE** | Highlight Objects | Shows all interactive objects (combine with G for positioning) |
| **D** | Debug Inventory | Logs inventory state to console |

**Recommended Combinations:**
- **G + W** = Best for creating walkable masks and finding spawn positions
- **G + SPACE** = Best for positioning items, NPCs, doors relative to grid
- **W + SPACE** = Verify objects are in walkable areas

### Walkable Areas Checklist

Use this checklist when adding walkable areas to your game:

**Planning Phase:**
- [ ] Identify which rooms need collision detection
- [ ] Sketch walkable vs blocked areas for each room
- [ ] Plan door entry/exit points

**Creation Phase:**
- [ ] Create room background art
- [ ] Create walkable mask (white = floor, black = obstacles)
- [ ] Visualize mask with tool: `python visualize_mask.py mask.png`
- [ ] Verify mask has 30-70% walkable area

**Implementation Phase:**
- [ ] Add `walkable_mask` parameter to Room creation
- [ ] Use debug grid (G + W) to find door spawn positions
- [ ] Update all door `player_target_position` values
- [ ] Test door transitions in both directions

**Testing Phase:**
- [ ] Click on floors → player walks there ✓
- [ ] Click on walls → player goes to nearest floor ✓
- [ ] Walk around → player stops at obstacles ✓
- [ ] Use doors → player spawns correctly ✓
- [ ] Check with W overlay → green areas match floors ✓

**Polish Phase:**
- [ ] Adjust mask for better player flow
- [ ] Widen narrow paths if players get stuck
- [ ] Ensure spawn positions feel natural
- [ ] Remove debug overlays from final build (optional)

### Quick Reference

**Create Mask:**
```bash
python create_example_mask.py  # See examples
# Create mask in image editor (white = floor, black = walls)
python visualize_mask.py your_mask.png  # Verify
```

**Add to Room:**
```python
room = Room(player, "room.png", "Name", "music.wav",
           walkable_mask="room_mask.png")
```

**Find Spawn Position:**
```
In game: Press G + W
Hover mouse on green area
Read "Spawn if feet here: (x, y)"
Use in door definition
```

**Debug:**
```
W = Show walkable overlay
G = Show positioning grid
G + W = Perfect for testing walkable areas
```

---

**Walkable areas are optional but highly recommended for polished, professional-feeling games.**

**For complete technical documentation, see `docs/walkable_areas/` directory.**
