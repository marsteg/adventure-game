# Mouse Spawn Calculator - Quick Guide

## The Problem It Solves

**Before:** "I want the player's feet at (569, 574), what spawn position do I use?"

**Now:** Just hover your mouse at (569, 574) and read the answer!

## How It Works

### When you hover your mouse, the info box shows:

```
┌────────────────────────────────────┐
│ Mouse (Feet): (569, 574)           │ ← Where you're pointing
│ Percentage: (44.5%, 86.2%)         │
│                                    │
│ Spawn if feet here: (544, 499)    │ ← Use in door code! (cyan)
│ Percentage: (42.5%, 74.9%)         │
│                                    │
│ at_percentage_width(42.5)          │ ← Copy to clipboard
│ at_percentage_height(74.9)         │
└────────────────────────────────────┘
```

## Perfect Workflow for Door Spawns

### Step 1: Find Where You Want Feet
```
Press G (enable grid)
Press W (show walkable areas)
Navigate to target room
```

### Step 2: Point at Desired Foot Position
```
Hover mouse over GREEN (walkable) area
Find a good spot where player should stand
```

### Step 3: Read Spawn Position
```
Look at info box:
"Spawn if feet here: (544, 499)" ← THIS is your door spawn!
```

### Step 4: Use in Code
```python
# Copy the spawn position directly
my_door = Door(
    50, 350, 80, 120,
    "assets/doors/door.png",
    "My Door",
    target_room,
    (544, 499),  # ← Paste spawn position here
    False, None
)

# Or use percentages
my_door = Door(
    ...,
    target_room,
    (at_percentage_width(42.5), at_percentage_height(74.9)),
    ...
)
```

## Visual Example

```
You hover here (green crosshair):
         ↓
    ════╬════  (569, 574) ← "Mouse (Feet)"
         ║

Info box calculates spawn:
    (544, 499) ← "Spawn if feet here"

If you use (544, 499) in door:

    ┌────────┐  (544, 499) ← Spawn position (cyan square)
    │        │
    │ Player │
    │        │
    └───┬────┘
        ↓
    ════╬════  (569, 574) ← Feet land here (blue circle)
```

## The Math (Automatic)

```
Player sprite: 50×75 pixels

Your mouse at:        (569, 574)
Subtract width/2:      -25
Subtract height:             -75
                      ─────────
Spawn position:       (544, 499)
```

You don't need to calculate! Just read from the info box.

## Color Coding

| Color | Text | What It Means |
|-------|------|---------------|
| White | "Mouse (Feet)" | Current cursor position |
| **Cyan** | "Spawn if feet here" | **USE THIS in door code** |
| Yellow | `at_percentage_...` | Ready-to-copy functions |

## Common Use Cases

### Case 1: New Door Spawn
**Goal:** Create door that spawns player in center of room

```
1. Press G + W in target room
2. Hover mouse at center of walkable floor
3. Read "Spawn if feet here: (640, 450)"
4. Use (640, 450) in door definition ✓
```

### Case 2: Fix Broken Door
**Goal:** Player spawns in wall, need to fix

```
1. Press G + W in problem room
2. Hover mouse over GREEN walkable area
3. Read "Spawn if feet here: (200, 500)"
4. Update door spawn to (200, 500) ✓
```

### Case 3: Precise Positioning
**Goal:** Player should spawn next to an object

```
1. Press G + W
2. Press SPACE (show interactive objects)
3. Hover next to object on green area
4. Read spawn position from info box
5. Use in door ✓
```

## Tips

1. **Always check walkable overlay** (W key) when choosing spawn
2. **Point at green areas** - spawn calculation assumes you want walkable
3. **Cyan text is your answer** - that's the spawn position to copy
4. **Test after setting** - go through door and verify with G key
5. **Spawn position = top-left** of sprite, feet = bottom-center

## Verification

After setting door spawn:
```
1. Go through door
2. Press G
3. Check cyan SPAWN marker matches what you set ✓
4. Check blue FEET marker is on green walkable area ✓
```

## Real Example

```python
# Before: Player spawns in wall
shop_return = Door(..., tourist_shop, (700, 350), ...)

# Process:
# 1. Press G + W in Tourist Shop
# 2. Hover over walkable floor area
# 3. Info shows: "Spawn if feet here: (544, 499)"

# After: Fixed!
shop_return = Door(..., tourist_shop, (544, 499), ...)
```

## Quick Reference

### What You See:
- Green crosshair = Where you're pointing (feet position)
- Cyan text = Spawn position to use in code
- Blue circle = Actual player feet (when player is there)
- Cyan square = Actual spawn point (when player is there)

### What to Copy:
```
From info box:
"Spawn if feet here: (544, 499)"
                     ^^^^^^^^^^^
                     Copy this!
```

Or:
```
"at_percentage_width(42.5)"
"at_percentage_height(74.9)"
    Copy these values!
```

---

**Now you can point where you want feet, and instantly know the spawn position!**

Press **G** and hover to try it! 🎯
