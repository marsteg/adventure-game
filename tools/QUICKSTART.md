# Asset Generator Tool

AI-powered asset generation tool for the Point & Click Adventure Game Engine. Generate NPCs, rooms, items, and doors using Hugging Face's free unlimited API with consistent, customizable art styles.

## Setup 

### 1. **Install Dependencies**
   ```bash
   pip install 'numpy<2'
   pip install -r tools/requirements.txt
   ```
**Key dependencies:** `huggingface_hub`, `python-dotenv`, `Pillow`, `PyYAML`, `rembg` (for background removal)

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

### 4. **Configure Your Game's Art Style** 
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
