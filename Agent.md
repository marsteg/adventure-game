# Point & Click Adventure Game Engine - Agent Guide

## Overview

This is a comprehensive Point & Click Adventure Game Engine built with PyGame. This guide will teach you how to create your own adventure games using this engine framework.

## Engine Architecture

The engine uses a **component-based architecture** where all interactive objects inherit from a `RectShape` base class. The core components are:

- **Rooms**: Game locations/scenes
- **NPCs**: Interactive characters with dialog systems
- **Items**: Collectible objects with inventory management
- **Actions**: Interactive objects (buttons, levers, puzzles)
- **Doors**: Navigation between rooms
- **Player**: Character with pathfinding and animations

## Minimum Required Information from User

**Before starting any game creation, agents MUST collect this essential information from the user:**

### 1. Visual Style (Art Direction)
**Required**: A clear description of the game's visual aesthetic

**Examples**:
- "comic book style" - Bright colors, bold outlines, cartoon-like characters
- "realistic mysterious" - Photorealistic backgrounds, detailed character sprites, dark atmosphere
- "pixel art retro" - 8-bit or 16-bit style graphics, limited color palette
- "hand-drawn sketchy" - Pencil/ink drawing style, rough textures
- "minimalist modern" - Clean lines, simple shapes, limited color scheme
- "gothic dark fantasy" - Medieval themes, muted colors, atmospheric lighting
- "sci-fi futuristic" - Metallic textures, neon colors, high-tech environments

### 2. Dialog Tone and Writing Style
**Required**: The overall mood and personality of character interactions

**Examples**:
- "funny/comedic" - Humorous dialogue, witty banter, lighthearted interactions
- "serious/dramatic" - Formal speech, important themes, emotional weight
- "satirical" - Social commentary, ironic humor, parody elements
- "mysterious/cryptic" - Vague hints, riddles, ambiguous statements
- "casual/friendly" - Conversational tone, everyday language, approachable
- "formal/academic" - Proper grammar, sophisticated vocabulary
- "quirky/eccentric" - Unusual character traits, unexpected responses

### 3. Story Synopsis
**Required**: A brief description of the game's plot and setting (2-4 sentences)

**Should Include**:
- **Setting**: Where and when the story takes place
- **Main Character**: Who the player controls (if specified)
- **Central Conflict**: The main problem or goal
- **Basic Premise**: What the player is trying to accomplish

**Example Synopsis**:
*"A young detective investigates mysterious disappearances in a small Victorian town. The player must explore haunted locations, interview eccentric townspeople, and solve puzzles to uncover a supernatural conspiracy. Each clue leads deeper into the town's dark secrets and ancient curse."*

### 4. Optional Additional Context
**Helpful but not required**:
- Preferred game length (short/medium/long)
- Specific themes or messages
- Target difficulty level
- Any special mechanics desired

---

## Creating a New Game - Process Overview

### 1. Keep the Engine Framework (DO NOT MODIFY)
These files contain the engine code and should remain unchanged:
- `constants.py` - Game configuration
- `room.py` - Room management system
- `npc.py` - Character system
- `item.py` - Item system
- `action.py` - Interactive object system
- `door.py` - Navigation system
- `inventory.py` - Inventory management
- `ui.py` - Rendering and UI systems
- `actionfuncs.py` - Action function library
- `dialogfuncs.py` - Dialog function library

### 2. Replace All Game Content
- Replace all assets in `assets/` directories
- Rewrite the game content section in `main.py` (keep pygame setup, replace room creation)
- Create new dialog YAML files
- Delete existing `save.yaml`

### 3. Asset Requirements and Organization

#### Required Asset Structure:
```
assets/
├── rooms/           # Background images (PNG/JPG)
├── npcs/           # Character sprites (PNG with transparency)
├── items/          # Collectible item images (PNG)
├── actions/        # Interactive object sprites (PNG)
├── doors/          # Door/entrance graphics (PNG, can be invisible)
├── player/         # Player character animations
│   ├── daisy_waiting.png      # Idle animation
│   ├── daisy_walking.png      # Walking sprite
│   └── walking/               # Directional animations
│       ├── left0.png - left5.png   # Left walking frames
│       └── right0.png - right5.png # Right walking frames
├── sounds/
│   ├── background/  # Music tracks (WAV/OGG)
│   ├── dialogs/     # Voice acting files (WAV)
│   ├── doors/       # Door sound effects (WAV)
│   ├── actions/     # Interaction sounds (WAV)
│   └── items/       # Item pickup/use sounds (WAV)
├── dialogs/         # YAML conversation files
└── menu/           # UI graphics (buttons, etc.)
```

#### Asset Guidelines:
- **Images**: PNG format recommended, use transparency for sprites
- **Audio**: WAV format for compatibility
- **Backgrounds**: Will be automatically scaled to screen size (1024x768)
- **Sprites**: Size according to your game's scale and style
- **Player Animation**: Requires 6 frames each for left/right walking

## Code Patterns and Examples

### ⚠️ **CRITICAL: Code Organization Order**

**Always define objects in this order for clean dependencies:**

```python
def create_your_game_content(player, inventory):
    # 1. ROOMS - Define all rooms first
    room1 = Room(player, "bg1.png", "Room 1", "music1.wav")
    room2 = Room(player, "bg2.png", "Room 2", "music2.wav")

    # 2. ITEMS - Create all items next
    key_item = Item(x, y, w, h, "key.png", "Magic Key")

    # 3. NPCs - Define NPCs before Actions (so NPCs can be used as keys)
    merchant = NPC(x, y, w, h, "merchant.png", "Merchant", True, key_item, WHITE, "merchant.yaml")

    # 4. ACTIONS - Create actions (can use NPCs as keys)
    locked_chest = Action(x, y, w, h, "chest.png", "Treasure Chest", True, merchant)

    # 5. DOORS - Create doors last (can reference all other objects as keys)
    secret_door = Door(x, y, w, h, "door.png", "Secret Door", room2, (x, y), True, locked_chest)
```

**Why This Order Matters:**
- **NPCs as Keys**: Actions and Doors can use NPCs as unlock keys
- **Clean Dependencies**: No need for messy post-creation assignments like `object.key = other_object`
- **Clear Code Flow**: Easy to understand object relationships
- **Maintainable**: Modifications are straightforward when dependencies are clear

### Room Creation Pattern
```python
# Create a room (with optional walkable mask)
room_name = Room(player_group, "background_image.png", "Room Name", "background_music.wav",
                walkable_mask="room_mask.png")  # Optional: Restrict player movement

# Add to global registry (automatic)
# Access later via Room.rooms["Room Name"]
```

**⚠️ IMPORTANT: Walkable Areas System**

For realistic collision detection and preventing players from walking through walls/furniture:

- Add `walkable_mask` parameter with PNG mask (white=walkable, black=blocked)
- Use debug tools: Press **W** to visualize walkable areas, **G** for positioning grid
- **See WALKABLE_AREAS_AGENT_GUIDE.md for complete documentation on:**
  - Creating walkable masks in image editors
  - Finding valid door spawn positions
  - Using debug tools (G/W keys)
  - Troubleshooting walkable areas
  - Step-by-step workflow and examples

**Quick Start:**
```python
# Generate example masks
python create_example_mask.py

# Visualize a mask
python visualize_mask.py room_mask.png

# Add to room
room = Room(player, "room.png", "Name", "music.wav",
           walkable_mask="assets/rooms/masks/room_mask.png")

# Find door spawn with debug grid (in-game: Press G + W)
# Hover on green area, read "Spawn if feet here" position
```

### Item Creation Pattern
```python
# Create a collectible item
item = Item(x, y, width, height, "item_image.png", "Item Name",
           description="Item description text",
           voice_file="assets/sounds/items/item_description.wav",
           action_funcs=[],  # Functions to run when picked up
           self_destruct=False)  # True for consumable items

# Add to room
room_name.items.add(item)
```

### NPC Creation Pattern
```python
# Create an NPC with dialog (Define before Actions for use as keys)
npc = NPC(x, y, width, height, "npc_sprite.png", "NPC Name",
          locked=True,  # Requires key to interact
          key=some_item_object,  # Item required to unlock
          speech_color=constants.WHITE,
          dialog_file="assets/dialogs/npc_dialog.yaml")

# Add to room
room_name.npcs.add(npc)
```

### Action Creation Pattern
```python
# Create an interactive object (NPCs must be defined first to use as keys)
action = Action(x, y, width, height, "action_image.png", "Action Name",
               locked=True,
               key=required_npc_or_item,  # Can be NPC or Item
               description_locked="Can't use this yet",
               description_unlocked="You can use this now",
               action_funcs=[
                   actionfuncs.LogText("Action performed!"),
                   actionfuncs.PlaySound("assets/sounds/actions/click.wav"),
                   actionfuncs.UnlockDoor("Door Name")
               ])

# Add to room
room_name.actions.add(action)
```

### Door Creation Pattern
```python
# Create a door/transition (Define last to reference all other objects as keys)
door = Door(x, y, width, height, "door_image.png", "Door Name",
           target_room_object,  # Reference to actual room object
           (target_x, target_y),  # Player position in target room
           locked=True,
           key=door_key_object)  # Item, Action, or NPC required to unlock

# Add description
door.add_description("Locked message", "Unlocked message",
                    "locked_sound.wav", "unlocked_sound.wav")

# Add to room
room_name.doors[door.name] = door
```

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

## Dialog System

### YAML Dialog File Structure

**Key Requirements:**
- Always use `start:` as initial state name
- Every NPC needs a dedicated `bye:` state with sound file
- Use `ChangeDialog: [NPCName, state]` array format
- Exit choices go to `bye` state, never direct `ExitDialog`

```yaml
# assets/dialogs/character_name.yaml
start:
  line: "Hello! Welcome to my shop."
  speaker: "Shopkeeper"
  sound: "assets/sounds/dialogs/shopkeeper_hello.wav"
  duration: 3
  answers:
    - line: "What do you sell?"
      actionfuncs:
        - ChangeDialog:
          - Shopkeeper
          - shop_inventory
    - line: "I need to go."
      actionfuncs:
        - ChangeDialog:
          - Shopkeeper
          - bye

shop_inventory:
  line: "I sell magical items and potions."
  speaker: "Shopkeeper"
  sound: "assets/sounds/dialogs/shopkeeper_items.wav"
  duration: 4
  answers:
    - line: "I'll take a potion."
      actionfuncs:
        - TakeItemString:
          - Gold Coin
          - no_money
          - purchase_complete
    - line: "Maybe later."
      actionfuncs:
        - ChangeDialog:
          - Shopkeeper
          - bye

no_money:
  line: "You don't have enough gold!"
  speaker: "Shopkeeper"
  sound: "assets/sounds/dialogs/shopkeeper_no_money.wav"
  duration: 3
  exit:
    ExitDialog: start

purchase_complete:
  line: "Excellent choice! Here's your potion."
  speaker: "Shopkeeper"
  sound: "assets/sounds/dialogs/shopkeeper_purchase.wav"
  duration: 4
  answers:
    - line: "Thank you!"
      actionfuncs:
        - GiveItemString: "Health Potion"
        - ChangeDialog:
          - Shopkeeper
          - bye

bye:
  line: "Come back anytime!"
  speaker: "Shopkeeper"
  sound: "assets/sounds/dialogs/shopkeeper_farewell.wav"
  duration: 2
  exit:
    ExitDialog: start
```

### Dialog Functions Available:
- `ChangeDialog: [NPCName, new_state]` - Switch to conversation branch
- `ExitDialog: start` - End conversation (only use in `exit:` blocks)
- `TakeItemString: [item_name, failure_state, success_state]` - Conditional item removal
- `GiveItemString: "Item Name"` - Add item to inventory
- `UnlockNPC: "NPC Name"` - Unlock another character

### ⚠️ **CRITICAL Dialog Rules:**
- ✅ Always use dedicated `bye` states for conversation exits
- ✅ `ChangeDialog: [NPCName, state]` array format required
- ✅ `line: "Single string"` recommended over arrays
- ✅ `TakeItemString: [item, failure, success]` with both states implemented
- ❌ Never use `ExitDialog` directly in answer choices

### Action Functions Available:
- `LogText("message")` - Print to console
- `ChangePicture("new_image.png")` - Change object's sprite
- `PlaySound("sound_file.wav")` - Play audio effect
- `UnlockDoor("Door Name")` - Open a locked door
- `GiveItem(item_object)` - Add item to inventory
- `TakeItem(item_object)` - Remove item from inventory
- `DestroyItem(item_object)` - Permanently remove item
- `ActionChangeDialog("NPC Name", "new_state")` - Change NPC's dialog state

## ⚠️ CRITICAL: Lock/Key System Implementation

### Understanding the Lock/Key Mechanism

The engine uses a **key-based locking system** where objects can be locked and require specific keys:

**Objects that can be locked:**
- **NPCs** - Require items to talk to them
- **Actions** - Require items to activate them
- **Doors** - Require items or actions to open them

**Objects that can be keys:**
- **Items** - Physical objects in inventory
- **Actions** - Interactive objects that must be activated first

### Lock/Key Setup Patterns

#### 1. Item-Locked Door
```python
# Door requires an item to unlock
key_item = Item(x, y, w, h, "key.png", "Magic Key")
locked_door = Door(x, y, w, h, "door.png", "Locked Door",
                  target_room, (x, y), locked=True, key=key_item)
```

#### 2. Action-Unlocked Door (Quest Progression)
```python
# Create the action first
puzzle_action = Action(x, y, w, h, "puzzle.png", "Ancient Puzzle")

# Door requires the action to be activated first
quest_door = Door(x, y, w, h, "door.png", "Quest Door",
                 target_room, (x, y), locked=True, key=puzzle_action)

# Action unlocks the door when activated
puzzle_action.add_function(actionfuncs.UnlockDoor, puzzle_action, quest_door)
```

#### 3. Item-Locked NPC
```python
# NPC requires item to unlock conversation
unlock_item = Item(x, y, w, h, "gift.png", "Special Gift")
locked_npc = NPC(x, y, w, h, "npc.png", "Merchant",
                locked=True, key=unlock_item, ...)
```

#### 4. Item-Locked Action
```python
# Action requires item to activate
tool_item = Item(x, y, w, h, "tool.png", "Ancient Tool")
locked_action = Action(x, y, w, h, "machine.png", "Ancient Machine",
                      locked=True, key=tool_item, ...)
```

### UnlockDoor Function Requirements

**CRITICAL**: The `UnlockDoor` function checks if the door's key matches the unlocking action:

```python
# This is how UnlockDoor works internally:
def UnlockDoor(action, door):
    if door.key != action:  # Key must match!
        print("Wrong key")
        return
    door.unlock(door.key)
```

**Correct Implementation:**
```python
# 1. Create action that will unlock the door
vase_action = Action(x, y, w, h, "vase.png", "Ancient Vase")

# 2. Create door with action as key
temple_door = Door(x, y, w, h, "door.png", "Temple Door",
                  target_room, (x, y), locked=True, key=vase_action)

# 3. Action unlocks its own door when activated
vase_action.add_function(actionfuncs.UnlockDoor, vase_action, temple_door)
```

### Quest Progression Chain Example

```python
# Step 1: Collect item
brochure = Item(x, y, w, h, "brochure.png", "Guide Book")

# Step 2: Use item to unlock puzzle
puzzle = Action(x, y, w, h, "puzzle.png", "Ancient Puzzle",
               locked=True, key=brochure)

# Step 3: Puzzle unlocks door when solved
secret_door = Door(x, y, w, h, "door.png", "Secret Passage",
                  next_room, (x, y), locked=True, key=puzzle)

# Step 4: Connect the chain
puzzle.add_function(actionfuncs.UnlockDoor, puzzle, secret_door)
```

### Lock System Best Practices

1. **Always set the key object** when creating locked doors/NPCs/actions
2. **Use the unlocking object as the key** (not a different object)
3. **Test the progression chain** to ensure proper unlock sequence
4. **Provide clear visual/text feedback** about what's needed to unlock
5. **Document the progression** for complex multi-step puzzles

## Game Creation Workflow

### Step 1: Plan Your Game
1. **Story Concept**: Define plot, characters, and setting
2. **Room Layout**: Sketch your game world and connections
3. **Character Roles**: Plan NPCs and their dialog purposes
4. **Puzzle Design**: Design item-based puzzles and progression
5. **Asset List**: Inventory all images and sounds needed

### Step 2: Create Assets
1. **Art Creation**: Create all required images following the directory structure
2. **Audio Production**: Record/source music, voice acting, and sound effects
3. **Dialog Writing**: Write all conversations and branching choices
4. **File Organization**: Place all assets in correct directories

### Step 3: Implement Game Content
1. **Clear main.py**: Remove existing room creation code (keep pygame setup)
2. **Create Rooms**: Instantiate all your rooms with backgrounds and music
3. **Populate Rooms**: Add NPCs, items, actions, and doors to each room
4. **Set Starting Point**: Define initial room and player position
5. **Create Dialog Files**: Implement all YAML conversation files

### Step 4: Testing and Polish
1. **Test Interactions**: Verify all NPCs, items, and actions work
2. **Test Navigation**: Ensure all doors connect properly
3. **Test Dialogs**: Check all conversation branches and effects
4. **Test Inventory**: Verify item pickup, use, and combinations
5. **Audio Check**: Ensure all sounds and voices play correctly

## Advanced Features

### Item Combinations
Items can be combined by dragging one onto another:
```python
# In item creation, specify what it combines with
item1.combinable_with = ["Item2 Name"]
item2.combinable_with = ["Item1 Name"]

# Define what happens in action_funcs when combined
combined_result = Item(...)  # The resulting item
```

### Multi-line Dialogs
NPCs can speak multiple lines in sequence, but **use with caution**:
```yaml
conversation_state:
  line:
    - "This is the first line."
    - "This is the second line."
    - "This is the third line."
  speaker: "Character"
  sound: "assets/sounds/dialogs/character_multiline.wav"
  # Single sound file for entire sequence
```

**⚠️ IMPORTANT: Multi-line Dialog Limitations:**
- **Compatibility Issues**: Multi-line arrays can cause problems with dialog processing in some contexts
- **Recommended Approach**: Use single-line strings for better reliability
- **Alternative**: Combine multiple thoughts into one longer line with proper punctuation
- **If Using Arrays**: Test thoroughly to ensure proper dialog flow

**Preferred Single-Line Format:**
```yaml
conversation_state:
  line: "This combines multiple thoughts into one clear, coherent statement that flows naturally."
  speaker: "Character"
  sound: "assets/sounds/dialogs/character_statement.wav"
```

### Conditional Dialog with TakeItemString

The `TakeItemString` function allows conditional dialog flow based on inventory:

```yaml
# Example: NPC requests an item
request_item:
  line: "Do you have the ancient coin I need?"
  speaker: "Merchant"
  sound: "assets/sounds/dialogs/merchant_request.wav"
  duration: 3
  answers:
    - line: "Yes, here it is!"
      actionfuncs:
        - TakeItemString:
          - Ancient Coin        # Item to remove from inventory
          - no_coin            # Dialog state if player doesn't have item
          - got_coin           # Dialog state if player has item
    - line: "Not yet."
      actionfuncs:
        - ChangeDialog:
          - Merchant
          - bye

# Failure state (player doesn't have the item)
no_coin:
  line: "You don't have the coin! Come back when you find it."
  speaker: "Merchant"
  sound: "assets/sounds/dialogs/merchant_no_coin.wav"
  duration: 3
  exit:
    ExitDialog: start

# Success state (player has the item - it gets removed)
got_coin:
  line: "Perfect! Thank you. Here's your reward."
  speaker: "Merchant"
  sound: "assets/sounds/dialogs/merchant_success.wav"
  duration: 4
  answers:
    - line: "What's my reward?"
      actionfuncs:
        - GiveItemString: "Magic Potion"
        - ChangeDialog:
          - Merchant
          - reward_given
```

**⚠️ CRITICAL: TakeItemString Format Requirements:**
- **Always use array format**: `[item_name, failure_state, success_state]`
- **Create both states**: You must implement both failure and success dialog states
- **Item is removed**: If player has the item, it's permanently removed from inventory
- **Automatic branching**: The engine automatically chooses which state to go to

### Invisible Interactions
Doors and actions can be invisible (no image) for hotspot areas:
```python
# Create invisible door by using transparent/empty image
invisible_door = Door(x, y, width, height, "", "Secret Passage", ...)
```

## Performance Considerations

- **Image Caching**: Engine automatically caches images to prevent reload lag
- **Audio Management**: Only one voice line plays at a time to prevent overlap
- **Lazy Loading**: UI elements are created as needed
- **Efficient Collision**: Uses pygame.Rect for fast interaction detection

## Best Practices

### Game Design:
1. **Dialog Exit Options**: EVERY dialog state with answers must include a way to exit immediately
2. **Clear Visual Feedback**: Use the "shine mode" (SPACE key) to help players find interactions
3. **Logical Puzzles**: Ensure item combinations and requirements make sense
4. **Voice Integration**: Align voice files with text for immersive experience
5. **Save Compatibility**: Test that your game state saves/loads correctly

### Code Organization:
1. **Proper Object Order**: Always define in order: Rooms → Items → NPCs → Actions → Doors
2. **Clean Dependencies**: Define NPCs before Actions so they can be used as keys without post-creation assignments
3. **Consistent Naming**: Use descriptive names for rooms, NPCs, and items
4. **Logical Progression**: Design item dependencies that create natural flow
5. **Error Handling**: Test edge cases like using items without required keys
6. **Audio Timing**: Match voice file durations to dialog text length

### Asset Management:
1. **File Naming**: Use consistent, descriptive filenames
2. **Image Optimization**: Balance quality and file size for performance
3. **Audio Quality**: Consistent volume levels across all sound files
4. **Backup Strategy**: Keep source files separate from game-ready assets

## Example Game Template

Here's a minimal game creation template for `main.py`:

```python
# [Keep all the pygame setup code from original main.py]

def create_game_content(player_group):
    """Create all rooms, NPCs, items, actions, and doors for your game"""

    # Create your first room
    starting_room = Room(player_group, "assets/rooms/forest.png", "Forest", "assets/sounds/background/nature.wav")

    # Add an NPC
    wizard = NPC(400, 300, 100, 150, "assets/npcs/wizard.png", "Old Wizard",
                locked=False, speech_color=constants.WHITE,
                dialog_file="assets/dialogs/wizard.yaml")
    starting_room.npcs.add(wizard)

    # Add an item
    magic_stone = Item(200, 400, 50, 50, "assets/items/stone.png", "Magic Stone",
                      description="A mysterious glowing stone")
    starting_room.items.add(magic_stone)

    # Add a door to next room
    cave_entrance = Door(600, 350, 80, 100, "assets/doors/cave.png", "Cave Entrance",
                        locked=True, key=magic_stone, target_room="Cave",
                        target_x=100, target_y=400)
    starting_room.doors.add(cave_entrance)

    # Create second room
    cave_room = Room(player_group, "assets/rooms/cave.png", "Cave", "assets/sounds/background/cave_ambient.wav")

    # Set starting position
    constants.current_room = Room.rooms["Forest"]
    constants.player.x = 300
    constants.player.y = 450

# Call your game creation function
create_game_content(player_group)
```

## Troubleshooting Common Issues

### Assets Not Loading:
- Check file paths are correct and case-sensitive
- Ensure image files are valid PNG/JPG format
- Verify audio files are WAV format

### Dialog Not Working:
- Validate YAML syntax (use online YAML validator)
- Check that dialog file path matches NPC creation
- Ensure speaker names match exactly

### Items Not Appearing:
- Verify item coordinates are within room boundaries
- Check that items are added to correct room's items group
- Ensure item images exist and load properly

### Navigation Issues:
- Confirm target room names match exactly (case-sensitive)
- Verify target coordinates are valid positions in destination room
- Check that doors are unlocked or have correct key items

This engine provides a robust foundation for creating engaging point-and-click adventure games. Focus on storytelling, puzzle design, and player experience while the engine handles the technical complexity.


## Implementation Notes

### Room Object Assignment
```python
# Use dictionary assignment syntax
room_name.npcs[npc.name] = npc
room_name.items[item.name] = item
room_name.actions[action.name] = action
room_name.doors[door.name] = door
```

### Update Intro Cutscene
**CRITICAL**: Update hardcoded intro in `textcutscene.py` lines 16-52:
```python
self.slides = [
    {
        "title": "Your Game Title",
        "text": ["Story lines here..."]
    }
]
```

## Troubleshooting Common Issues

### Assets & Files
- **Missing Assets**: Check file paths are case-sensitive, use PNG/WAV formats
- **Wrong Intro**: Update hardcoded content in `textcutscene.py` lines 16-52

### Dialog Issues
- **Dialog Loops**: Use dedicated `bye` states, never `ExitDialog` in answer choices
- **KeyError 'start'**: Ensure all dialog files use `start:` as initial state
- **ChangeDialog Errors**: Use array format `[NPCName, state]`
- **TakeItemString Errors**: Use `[item, failure_state, success_state]` format
- **Multi-line Problems**: Use single strings instead of arrays for `line:`

### Lock/Key Issues
- **Doors Won't Unlock**: Ensure door's key matches the unlocking action
- **Object Dependencies**: Define NPCs before Actions so they can be used as keys during creation

### Navigation & Items
- **Items Not Appearing**: Check coordinates are within room boundaries
- **Navigation Issues**: Verify room names and target coordinates are correct

## Asset Creation Notes

**⚠️ LIMITATION**: Claude Code cannot generate images or audio files.

### Asset Requirements
- **Images**: Room backgrounds (1024x768), character sprites, items, actions
- **Audio**: Background music, dialog voice files, sound effects (WAV format)
- **Sources**: AI generators, stock art, commission artists, or create your own

### Development Strategy
1. **Prototype**: Use existing engine assets as placeholders
2. **Replace**: Source final assets before release
3. **Test**: Verify all assets load correctly

---

**This documentation has been field-tested and verified to produce working games.**