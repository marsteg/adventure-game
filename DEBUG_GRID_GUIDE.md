# Debug Grid Feature - Positioning Guide

## Overview

The debug grid helps you easily position items, doors, NPCs, and actions in your game by showing:
- Coordinate grid overlay
- Percentage markers (for use with `at_percentage_width()` and `at_percentage_height()`)
- Real-time mouse position in both pixels and percentages
- Ready-to-copy function calls

## How to Use

### Toggle Grid On/Off
Press **G** during gameplay to toggle the debug grid.

### What You'll See

1. **Grid Lines** (gray)
   - Fine grid: every 50 pixels
   - Major grid: every 100 pixels (thicker, with labels)

2. **Percentage Markers** (yellow)
   - Vertical: 0%, 10%, 20%, ... 100% of width
   - Horizontal: 0%, 10%, 20%, ... 100% of height
   - These correspond to your helper functions!

3. **Inventory Boundary** (red line)
   - Shows where the playable area ends
   - Items/doors below this won't be reachable

4. **Mouse Info Box** (green crosshair + info panel)
   - Shows exact pixel coordinates
   - Shows percentage values
   - Shows ready-to-use function calls

### Example Info Box Display

When you hover at position (640, 333):
```
Position: (640, 333)
Percentage: (50.0%, 50.0%)

at_percentage_width(50.0)
at_percentage_height(50.0)
```

## Positioning Workflow

### For Items

1. Run the game: `python main.py`
2. Press **G** to enable grid
3. Navigate to the room where you want to place an item
4. Move your mouse to where the item should be
5. Note the percentage values from the info box
6. Copy the values to your code:

```python
# Example: Positioning a key at 35% width, 60% height
key = Item(
    at_percentage_width(35.0),   # Copy from info box
    at_percentage_height(60.0),  # Copy from info box
    40, 30,                      # width, height
    "assets/items/key.png",
    "Golden Key",
    True
)
```

### For Doors

Same process as items:

```python
door = Door(
    at_percentage_width(80.0),   # Position from grid
    at_percentage_height(45.0),  # Position from grid
    100, 150,                    # width, height
    "assets/doors/exit.png",
    "Exit",
    target_room,
    (at_percentage_width(20.0), at_percentage_height(50.0))  # spawn position in next room
)
```

### For NPCs

```python
librarian = NPC(
    at_percentage_width(50.0),
    at_percentage_height(40.0),
    80, 120,
    "assets/npcs/librarian.png",
    "Librarian"
)
```

### For Actions (Clickable Areas)

```python
bookshelf = Action(
    at_percentage_width(25.0),
    at_percentage_height(30.0),
    150, 200,
    "Bookshelf",
    my_action_function
)
```

## Tips & Tricks

### Quick Reference Points

Common positions for reference:
- **Center of screen**: 50%, 50%
- **Top left corner**: 0%, 0%
- **Top right corner**: 100%, 0%
- **Bottom center**: 50%, 100%

### Alignment

- Use the grid lines to align multiple objects
- Major grid lines (every 100px) help with spacing
- Percentage markers help maintain consistent layouts across different screen areas

### Testing Object Size

1. Enable grid
2. Place object at position
3. Check if it fits within desired grid cells
4. Adjust width/height parameters as needed

### Door Spawn Positions

When setting `player_target_position` for doors:
1. Enable grid in the **target room**
2. Find a good spawn position (usually near the door but facing into the room)
3. Use those percentage values

Example:
```python
# Door in Room A going to Room B
door_to_room_b = Door(
    at_percentage_width(90.0),    # Door position in Room A
    at_percentage_height(50.0),
    80, 120,
    "assets/doors/door.png",
    "To Room B",
    room_b,
    # Player spawns in Room B at these coordinates:
    (at_percentage_width(15.0), at_percentage_height(50.0))
)
```

## Combining with Other Debug Features

You can use multiple debug tools together:

### Grid + Walkable Areas
```
Press G - see positioning grid
Press W - see walkable areas overlay
```

This helps you:
- Position items within walkable areas
- See if doors are in accessible locations
- Verify NPCs are standing on walkable ground

### Grid + Interactive Objects
```
Press G - see positioning grid
Press SPACE - highlight all interactive objects
```

This helps you:
- See spacing between objects
- Check if objects overlap
- Verify object placement

## Common Issues

### "Can't see the grid"
- Make sure you pressed **G** to enable it
- Grid only shows in the playable area (not in menus)
- Check console for "Debug grid: ON" message

### "Info box appears in wrong position"
- Info box automatically repositions to stay on screen
- It will appear near your mouse cursor
- May shift left/up if cursor is near screen edges

### "Grid interferes with gameplay"
- Simply press **G** again to toggle it off
- Grid is only visible when enabled, won't affect saved games or exports

### "Percentages don't match my code"
- Make sure you're using `at_percentage_width()` for X coordinates
- Make sure you're using `at_percentage_height()` for Y coordinates
- `at_percentage_height()` uses playable height (excludes inventory bar)

## Keyboard Shortcuts Summary

| Key | Function |
|-----|----------|
| **G** | Toggle debug grid on/off |
| **W** | Toggle walkable areas overlay |
| **SPACE** | Highlight interactive objects |
| **D** | Debug inventory state |
| **S** | Open save menu |
| **L** | Open load menu |

## Example: Complete Item Placement

Let's say you want to add a book to the library:

1. **Run game**: `python main.py`
2. **Enable grid**: Press `G`
3. **Navigate to library room**
4. **Find position**: Move mouse to desired location
   - Info box shows: `at_percentage_width(42.5), at_percentage_height(65.0)`
5. **Open game.py** in editor
6. **Add item code**:
```python
ancient_book = Item(
    at_percentage_width(42.5),
    at_percentage_height(65.0),
    50, 40,
    "assets/items/book.png",
    "Ancient Book",
    True
)
ancient_book.add_description("A dusty tome", "assets/sounds/items/book.wav")
library.items[ancient_book.name] = ancient_book
```
7. **Save and restart game** to see the item

## Advanced: Pixel-Perfect Positioning

If you need exact pixel coordinates instead of percentages:

```python
# Use the pixel values directly
key = Item(640, 333, 40, 30, "assets/items/key.png", "Key", True)
```

But percentages are recommended because they:
- Scale better if you change screen resolution
- Are easier to reason about ("centered at 50%")
- Work consistently across different rooms

---

**Feature added in commit**: Debug grid positioning tool
