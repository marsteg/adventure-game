# Debug Grid Visual Reference

## What You'll See

```
┌──────────────────────────────────────────────────────────────┐
│ 0%    10%   20%   30%   40%   50%   60%   70%   80%   90% 100%│ ← Yellow % markers
├──────────────────────────────────────────────────────────────┤
│ 0│  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼─┤ ← 50px grid (gray)
│10%  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼─┤
│20%  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼─┤
│30%  │  │  │  │  │  ┌──────────────┐   │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──│ Position:    │───┼──┼──┼──┼──┼──┼──┼─┤
│40%  │  │  │  │  │  │ (640, 333)   │   │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──│ Percentage:  │───┼──┼──┼──┼──┼──┼──┼─┤
│50%  │  │  │  │  │  │ (50.0%, 50.0%)│  │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──│              │───┼──┼──┼──┼──┼──┼──┼─┤
│60%  │  │  │  │  ╳  │at_percentage_│   │  │  │  │  │  │  │ │ ← Crosshair
│  ├──┼──┼──┼──┼──┼──│width(50.0)   │───┼──┼──┼──┼──┼──┼──┼─┤
│70%  │  │  │  │  │  │at_percentage_│   │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──│height(50.0)  │───┼──┼──┼──┼──┼──┼──┼─┤
│80%  │  │  │  │  │  └──────────────┘   │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼─┤
│90%  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ │
│  ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼─┤
│100% │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ │
├════════════════════════════════════════════════════════════┤
│               INVENTORY BOUNDARY (RED LINE)                  │ ← 666px
├════════════════════════════════════════════════════════════┤
│  [inventory items displayed here]                           │
└──────────────────────────────────────────────────────────────┘
  ↑                                                           ↑
  0px                                                    1280px
```

## Grid Elements

### Coordinate Labels (white)
- Top edge: `0, 100, 200, 300...` (X coordinates)
- Left edge: `0, 100, 200, 300...` (Y coordinates)

### Percentage Markers (yellow)
- Top edge: `0%, 10%, 20%...100%` with yellow lines
- Left edge: `0%, 10%, 20%...100%` with yellow lines

### Grid Lines
- **Light gray** (every 50px): Fine positioning
- **Medium gray** (every 100px): Major divisions with labels

### Mouse Crosshair (green)
- Horizontal line: ─────╳─────
- Vertical line crossing through cursor
- Circle around exact point

### Info Box (green border, black bg)
```
┌──────────────────────────┐
│ Position: (640, 333)     │ ← Pixel coordinates
│ Percentage: (50.0%, 50.0%)│ ← Percentage values
│                          │
│ at_percentage_width(50.0)│ ← Copy this
│ at_percentage_height(50.0)│ ← Copy this
└──────────────────────────┘
```

### Inventory Boundary (red)
- Thick red line at y=666
- Label: "INVENTORY BOUNDARY"
- Objects below this are in UI space

### Help Text (bottom left)
```
┌─────────────────────────────────┐
│ GRID MODE - Press G to toggle  │
│ Click anywhere to see position  │
└─────────────────────────────────┘
```

## Color Coding

| Color | Element | Meaning |
|-------|---------|---------|
| Light Gray | Fine grid | 50px intervals |
| Medium Gray | Major grid | 100px intervals with labels |
| Yellow | % markers | 10% intervals (top/left) |
| Red | Boundary line | Inventory area starts |
| Green | Crosshair + box | Current mouse position |
| White | Labels | Coordinate numbers |

## Example Scenarios

### Placing a Door on the Right Wall
```
Mouse at: (1150, 350)
Percentage: (89.8%, 52.6%)

Use: at_percentage_width(89.8), at_percentage_height(52.6)
```

### Centering an NPC
```
Mouse at: (640, 350)
Percentage: (50.0%, 52.6%)

Use: at_percentage_width(50.0), at_percentage_height(52.6)
```

### Item Near Bottom Left
```
Mouse at: (200, 600)
Percentage: (15.6%, 90.0%)

Use: at_percentage_width(15.6), at_percentage_height(90.0)
```

## Quick Tips

1. **Major Grid Lines** = easy reference points (every 100px)
2. **Yellow % Markers** = match your percentage functions
3. **Hover anywhere** = instant position feedback
4. **Green crosshair** = precise targeting
5. **Info box** = copy-paste ready code

---

Press **G** in-game to see this live!
