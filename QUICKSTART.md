# Quick Start Guide - Asset Generator

## ✅ Fixed NumPy Issue!

The tool now works perfectly even with the NumPy compatibility issue. Background removal is optional.

## Setup (30 seconds)

1. **Get Free API Key**
   - Go to: https://platform.stability.ai/
   - Sign up (free)
   - Get API key (25 images/month free)

2. **Configure**
   ```bash
   cp tools/config.yaml.example tools/config.yaml
   nano tools/config.yaml  # Add your API key
   ```

3. **Done!** You're ready to generate assets.

## Usage

### Interactive Mode (Easiest)
```bash
python3 tools/asset_generator.py --interactive
```

### Command Line
```bash
# Generate NPC
python3 tools/asset_generator.py npc "friendly wizard with staff" wizard

# Generate Room
python3 tools/asset_generator.py room "dark mysterious cave" cave_dark

# Generate Item
python3 tools/asset_generator.py item "golden key" key_gold

# Check usage
python3 tools/asset_generator.py --check-usage
```

## What Works Now

✅ Image generation (Stability AI)
✅ Automatic file naming
✅ Saves to correct folders
✅ Usage tracking
✅ Interactive mode
✅ Command-line mode
✅ Template system

⚠️ Background removal disabled (optional feature)
   - Tool works perfectly without it!
   - Only needed for NPCs/items
   - To enable: `pip install 'numpy<2' && pip install rembg`

## Example Workflow

```bash
# 1. Check remaining quota
python3 tools/asset_generator.py --check-usage
# Output: Monthly usage: 0/25 (Remaining: 25)

# 2. Generate assets
python3 tools/asset_generator.py npc "elderly librarian" librarian_old
python3 tools/asset_generator.py room "ancient library" library_ancient
python3 tools/asset_generator.py item "magic book" book_magic

# 3. Assets saved to:
# assets/npcs/librarian_old.png
# assets/rooms/library_ancient.png
# assets/items/book_magic.png
```

## Tips

1. **Be specific** - "friendly shopkeeper with apron" not just "person"
2. **Use style keywords** - "cartoon style", "illustrated", "detailed"
3. **Check usage** - Stay within 25/month limit
4. **Preview prompts** - Use `--list-templates` for ideas

## Need Help?

See `tools/README.md` for:
- Complete documentation
- Troubleshooting guide
- Advanced usage
- Prompt writing tips
- API configuration

---

**You're all set! Start generating assets for your adventure game! 🎮**
