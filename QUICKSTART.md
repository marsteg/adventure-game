# Quick Start Guide - Asset Generator

## ✅ Fixed NumPy Issue!

The tool now checks for NumPy compatibility and guides you to fix it if needed.

## Setup (2 minutes)

### 1. **Fix Dependencies**
   ```bash
   pip install 'numpy<2'
   pip install -r tools/requirements.txt
   ```

### 2. **Get Free API Key**
   - Go to: https://huggingface.co/settings/tokens
   - Click "New token" (select "Read" access)
   - Copy your token
   - **No credit card required!** Truly free and unlimited!

### 3. **Configure API**
   ```bash
   cp tools/config.yaml.example tools/config.yaml
   nano tools/config.yaml  # Add your Hugging Face API key
   ```

   Set `provider: "huggingface"` (already the default) and add your token:
   ```yaml
   provider: "huggingface"
   huggingface_api_key: "hf_your_token_here"
   ```

### 4. **Configure Your Game's Art Style** ⭐ NEW!
   ```bash
   cp tools/style_config.yaml.example tools/style_config.yaml
   nano tools/style_config.yaml  # Customize for your game
   ```

   **This is VERY important!** The style config controls:
   - ✅ 2D vs 3D style (avoid 3D renders)
   - ✅ Cartoon vs realistic
   - ✅ Color palette
   - ✅ Level of detail

   Edit `master_style.negative_keywords` to exclude unwanted styles like "3D render, CGI, photorealistic"

### 5. **Done!** You're ready to generate assets.

## Usage

### Interactive Mode (Easiest)
```bash
python3 tools/asset_generator.py --interactive
```

### Command Line
```bash
# Generate NPC with your style
python3 tools/asset_generator.py npc "zombie character" zombie

# Generate Room
python3 tools/asset_generator.py room "dark mysterious cave" cave_dark

# Check usage
python3 tools/asset_generator.py --check-usage
```

## What Works Now

✅ Image generation (Hugging Face - FREE & UNLIMITED!)
✅ Automatic file naming
✅ Saves to correct folders
✅ Usage tracking
✅ Interactive mode
✅ Command-line mode
✅ Template system
✅ Centralized style configuration
✅ Negative prompts to avoid unwanted styles
✅ Provider switching (Hugging Face or Stability AI)

⚠️ Background removal requires NumPy 1.x
   - To enable: `pip install 'numpy<2' && pip install rembg`

## Fixing Style Issues

### Problem: "My zombie looks 3D rendered instead of cartoon!"

**Solution:** Edit `tools/style_config.yaml`

1. Update `master_style.negative_keywords`:
   ```yaml
   negative_keywords: "3D render, photorealistic, realistic, cinema4d, unreal engine, 3D animated, CGI, octane render, ray tracing, volumetric lighting, Pixar style"
   ```

2. Strengthen your positive style:
   ```yaml
   art_style: "2D cartoon illustration, hand-drawn style, flat colors, cel-shaded, bold outlines"
   detail_level: "simple, clean lines, NOT 3D rendered, NOT photorealistic"
   ```

3. Add reference games:
   ```yaml
   additional: "similar to Monkey Island, Day of the Tentacle, hand-painted adventure game"
   ```

### The Power of Negative Prompts

Negative keywords are CRITICAL! They tell the AI what to avoid:
- "3D render" → prevents CGI look
- "photorealistic" → prevents realistic style
- "octane render, ray tracing" → prevents modern 3D rendering
- "Pixar style, Disney 3D" → prevents 3D animation look

**Always specify what you DON'T want!**

## Example Workflow

```bash
# 1. Check remaining quota (not really needed for HF but shows tracking)
python3 tools/asset_generator.py --check-usage
# Output: Monthly usage: 0/999 (Remaining: 999)

# 2. Generate assets (all FREE with Hugging Face!)
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
3. **Unlimited generation** - Hugging Face has no credit limits!
4. **Preview prompts** - Use `--list-templates` for ideas
5. **Switch providers** - Set `provider: "stability"` in config.yaml if needed

## Need Help?

See `tools/README.md` for:
- Complete documentation
- Troubleshooting guide
- Advanced usage
- Prompt writing tips
- API configuration

---

**You're all set! Start generating assets for your adventure game! 🎮**
