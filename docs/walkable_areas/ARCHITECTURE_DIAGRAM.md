# Walkable Areas - Visual Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WALKABLE AREAS SYSTEM                     │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  1. ROOM WITH BACKGROUND IMAGE                                 │
│                                                                │
│     ┌──────────────────────────────────────┐                  │
│     │                                      │                  │
│     │  █████  [WALL]     [WALL]  █████    │                  │
│     │                                      │                  │
│     │         [WALKABLE FLOOR]             │                  │
│     │                                      │                  │
│     │  [TABLE]          👤          [BED]  │                  │
│     │                                      │                  │
│     │         [WALKABLE FLOOR]             │                  │
│     │                                      │                  │
│     │  █████  [WALL]     [WALL]  █████    │                  │
│     └──────────────────────────────────────┘                  │
│                  room_background.png                           │
└────────────────────────────────────────────────────────────────┘

                            ⬇

┌────────────────────────────────────────────────────────────────┐
│  2. WALKABLE MASK IMAGE (created by game designer)             │
│                                                                │
│     ┌──────────────────────────────────────┐                  │
│     │        WHITE = WALKABLE ✓            │                  │
│     │        BLACK/TRANSPARENT = BLOCKED ✗  │                  │
│     │                                      │                  │
│     │  ███████████████████████████████████ │  ← Black (walls) │
│     │  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█ │                  │
│     │  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█ │  ← White (floor) │
│     │  █░░██████░░░░░░░░░░░░░░░██████░░░█ │  ← Black (table) │
│     │  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█ │                  │
│     │  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█ │  ← White (floor) │
│     │  ███████████████████████████████████ │  ← Black (walls) │
│     └──────────────────────────────────────┘                  │
│                  room_mask.png                                 │
└────────────────────────────────────────────────────────────────┘

                            ⬇

┌────────────────────────────────────────────────────────────────┐
│  3. IN-GAME SYSTEM                                             │
│                                                                │
│  Player Clicks Position (x, y)                                 │
│         ⬇                                                      │
│  Room.find_nearest_walkable(x, y)                              │
│         ⬇                                                      │
│  Check mask pixel at (x, y):                                   │
│    • color.alpha > 128 → WALKABLE ✓ (return position)         │
│    • color.alpha ≤ 128 → BLOCKED ✗ (search for nearest)       │
│         ⬇                                                      │
│  If blocked, spiral search outward:                            │
│         ⬇                                                      │
│  Find nearest white pixel within 200px radius                  │
│         ⬇                                                      │
│  Player.set_target(walkable_position)                          │
│         ⬇                                                      │
│  Player walks to valid position! 🎮                            │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  4. DEBUG VISUALIZATION (Press W)                              │
│                                                                │
│     ┌──────────────────────────────────────┐                  │
│     │                                      │                  │
│     │  🟫🟫🟫🟫  (walls - dark)              │                  │
│     │                                      │                  │
│     │  🟩🟩🟩🟩🟩🟩  (floor - green overlay)   │                  │
│     │                                      │                  │
│     │  🟫 [TABLE] 👤 🟫      [BED] 🟫       │                  │
│     │                                      │                  │
│     │  🟩🟩🟩🟩🟩🟩  (floor - green overlay)   │                  │
│     │                                      │                  │
│     │  🟫🟫🟫🟫  (walls - dark)              │                  │
│     └──────────────────────────────────────┘                  │
│          Green = Where player can walk                         │
│          Dark = Where player cannot walk                       │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  CLICK BEHAVIOR EXAMPLES                                       │
│                                                                │
│  Example 1: Click on walkable floor                            │
│    User clicks: (640, 400) → on white mask pixel               │
│    → is_walkable() returns True                                │
│    → Player walks directly to (640, 400) ✓                     │
│                                                                │
│  Example 2: Click on table (blocked)                           │
│    User clicks: (640, 300) → on black mask pixel               │
│    → is_walkable() returns False                               │
│    → find_nearest_walkable() searches in spiral                │
│    → Finds (640, 380) is walkable (floor next to table)        │
│    → Player walks to (640, 380) instead ✓                      │
│                                                                │
│  Example 3: Click on wall (blocked)                            │
│    User clicks: (100, 100) → on black mask pixel               │
│    → is_walkable() returns False                               │
│    → find_nearest_walkable() searches in spiral                │
│    → Finds (150, 200) is walkable (floor near wall)            │
│    → Player walks to (150, 200) instead ✓                      │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  CODE FLOW                                                     │
│                                                                │
│  game.py:                                                      │
│  ┌──────────────────────────────────────────────┐             │
│  │ room = Room(player, "room.png", "Room",      │             │
│  │             "music.wav",                     │             │
│  │             walkable_mask="mask.png")  ←───┐ │             │
│  └──────────────────────────────────────────┼──┘             │
│                                             │                  │
│  room.py:                                   │                  │
│  ┌──────────────────────────────────────────▼──┐             │
│  │ def __init__(self, ..., walkable_mask=None): │             │
│  │     if walkable_mask:                        │             │
│  │         self._load_walkable_mask(...)  ←───┐ │             │
│  │                                            │ │             │
│  │ def is_walkable(self, pos):                │ │             │
│  │     color = self.walkable_mask.get_at(pos) │ │             │
│  │     return color.a > 128                   │ │             │
│  │                                            │ │             │
│  │ def find_nearest_walkable(self, pos):      │ │             │
│  │     if self.is_walkable(pos):              │ │             │
│  │         return pos                         │ │             │
│  │     # Spiral search...                     │ │             │
│  │     return nearest_walkable_pos            │ │             │
│  └─────────────────────────────────────────┼───┘             │
│                                             │                  │
│  main.py:                                   │                  │
│  ┌──────────────────────────────────────────▼──┐             │
│  │ # When player clicks:                       │             │
│  │ walkable_pos = active_room.find_nearest_    │             │
│  │                walkable(mouse_pos)          │             │
│  │ player.set_target(walkable_pos)             │             │
│  │                                             │             │
│  │ # Debug visualization (W key):              │             │
│  │ if SHOW_WALKABLE_AREA:                      │             │
│  │     active_room.draw_walkable_overlay(...)  │             │
│  └───────────────────────────────────────────────┘             │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  PIXEL ALPHA VALUES                                            │
│                                                                │
│  Alpha Channel determines walkability:                         │
│                                                                │
│  ┌──────────┬──────────┬──────────────────┐                   │
│  │ Alpha    │ Visible  │ Walkable?        │                   │
│  ├──────────┼──────────┼──────────────────┤                   │
│  │ 0        │ No       │ ✗ Blocked        │                   │
│  │ 50       │ Barely   │ ✗ Blocked        │                   │
│  │ 128      │ Half     │ ✗ Blocked        │                   │
│  │ 129      │ Half     │ ✓ Walkable       │  ← Threshold!    │
│  │ 200      │ Mostly   │ ✓ Walkable       │                   │
│  │ 255      │ Fully    │ ✓ Walkable       │                   │
│  └──────────┴──────────┴──────────────────┘                   │
│                                                                │
│  Examples:                                                     │
│    • White  (255, 255, 255, 255) → Walkable ✓                 │
│    • Black  (0, 0, 0, 255) → Walkable ✓ (if alpha=255)        │
│    • Black  (0, 0, 0, 0) → Blocked ✗ (alpha=0)                │
│    • Transparent (any, any, any, 0) → Blocked ✗               │
│                                                                │
│  Best Practice: Use white (255,255,255,255) for walkable      │
│                 Use transparent (0,0,0,0) for blocked         │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  SPIRAL SEARCH ALGORITHM                                       │
│                                                                │
│  When clicked position is not walkable:                        │
│                                                                │
│         ❌ Click here (on table)                               │
│         │                                                      │
│    5────4────3────2────1 ← Radius 1 (5px)                     │
│    │    │    │    │    │                                      │
│    6────5────4────3────2 ← Radius 2 (10px)                    │
│    │    │    │    │    │                                      │
│    7────6────5────4────3 ← Radius 3 (15px)                    │
│    │    │    │    │    │                                      │
│    8────7────6────5────4                                      │
│    │    │    │    │    │                                      │
│    9────8────7────6────✅ ← Found walkable! (floor)            │
│                                                                │
│  Search parameters:                                            │
│    • Step size: 5 pixels                                       │
│    • Angle step: 15 degrees (24 points per circle)            │
│    • Max radius: 200 pixels                                    │
│    • Returns first walkable point found                        │
│                                                                │
│  Code:                                                         │
│    for radius in range(1, 200, 5):  # Every 5 pixels          │
│        for angle in range(0, 360, 15):  # Every 15 degrees    │
│            check_x = x + radius * cos(angle)                   │
│            check_y = y + radius * sin(angle)                   │
│            if is_walkable((check_x, check_y)):                 │
│                return (check_x, check_y)  # Found it!          │
└────────────────────────────────────────────────────────────────┘
```
