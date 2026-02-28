# 🚶 Walkable Areas Feature

## Quick Start

Add walkable area restrictions to your rooms in 3 easy steps:

```python
# 1. Create a mask image (white = walkable, black = blocked)
# 2. Save it as PNG with transparency
# 3. Add to your room:

room = Room(player, "room.png", "Room Name", "music.wav",
            walkable_mask="path/to/mask.png")
```

**Press W in-game** to visualize walkable areas!

---

## 📚 Documentation

- **[Complete Guide](WALKABLE_AREAS_GUIDE.md)** - Full tutorial with examples
- **[Quick Reference](WALKABLE_AREAS_QUICKREF.md)** - One-page cheat sheet
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Technical details

---

## 🎨 Creating Masks

### Option 1: Use Image Editor (Recommended)

1. Open your room background in Photoshop/GIMP
2. Create new layer
3. Paint **white** where player can walk
4. Leave **transparent/black** where blocked
5. Save layer as PNG

### Option 2: Use Helper Script

```bash
# Generate example masks
python create_example_mask.py

# View a mask
python create_example_mask.py view mask.png
```

---

## 🎮 In-Game Controls

| Key | Function |
|-----|----------|
| **W** | Toggle walkable area visualization |
| **SPACE** | Show all interactive objects |
| **S** | Save game |
| **L** | Load game |

---

## ✨ Features

- ✅ Pixel-perfect collision detection
- ✅ Automatic nearest-point finding
- ✅ Visual debug overlay (press W)
- ✅ Backward compatible (optional feature)
- ✅ No performance impact
- ✅ Cached image loading
- ✅ Works with all room sizes

---

## 🎯 Example

```python
# Create room with walkable floor area only
tavern = Room(
    player,
    image="assets/rooms/tavern.png",
    name="Tavern",
    music="assets/sounds/tavern.wav",
    walkable_mask="assets/rooms/masks/tavern_mask.png"
)

# Player can now only walk on floor, not through walls or furniture!
```

---

## 📁 Recommended Structure

```
assets/rooms/
  ├── tavern.png
  ├── bedroom.png
  └── masks/
      ├── tavern_mask.png
      └── bedroom_mask.png
```

---

## 🔧 How It Works

**Mask Image:**
- White/visible pixels (alpha > 128) = **Walkable** ✓
- Black/transparent (alpha ≤ 128) = **Blocked** ✗

**Smart Clicking:**
- Click walkable area → player walks there
- Click blocked area → player walks to nearest valid point

**No Mask:**
- Room works normally (player can walk anywhere)
- Fully backward compatible!

---

## 🐛 Troubleshooting

**Player can't walk anywhere:**
- Your mask is all black/transparent
- Paint white areas for walkable zones

**Mask doesn't match room:**
- Press W to visualize
- Check file path is correct
- Verify PNG format

**Mask not loading:**
- Check console for error messages
- Verify file exists at specified path

---

## 📦 What's Included

- `room.py` - Core mask system
- `main.py` - Integration with game loop
- `create_example_mask.py` - Helper tool
- `WALKABLE_AREAS_GUIDE.md` - Complete tutorial
- `WALKABLE_AREAS_QUICKREF.md` - Quick reference
- `IMPLEMENTATION_SUMMARY.md` - Technical docs
- `example_mask.png` - Simple example
- `example_mask_complex.png` - Complex example

---

## 🚀 Get Started

1. **Read the guide**: Open [WALKABLE_AREAS_GUIDE.md](WALKABLE_AREAS_GUIDE.md)
2. **Generate examples**: Run `python create_example_mask.py`
3. **View examples**: Run `python create_example_mask.py view example_mask.png`
4. **Create your mask**: Use image editor to paint walkable areas
5. **Test in-game**: Add mask to room, press W to visualize

---

## 💡 Tips

- Start with generous walkable areas, refine later
- Use W key frequently to check alignment
- Keep masks simple at first
- Test by clicking on walls/obstacles
- Masks can be any size (auto-scaled)

---

**Happy game developing! 🎮**
