# Asset Generator Tool

AI-powered asset generation tool for the Point & Click Adventure Game Engine. Generate NPCs, rooms, items, and doors using Hugging Face's free unlimited API with consistent, customizable art styles.

## Features

✅ **FREE Unlimited AI Image Generation** - Uses Hugging Face FLUX.1-schnell model (no credit limits!)
✅ **Centralized Style Control** - Define your game's art style once in `style_config.yaml`
✅ **Negative Prompts** - Exclude unwanted styles (3D, photorealistic, CGI, etc.)
✅ **Configurable Dimensions** - Set default sizes per asset type, override per-generation
✅ **Automatic Background Removal** - Transparent backgrounds for NPCs and items
✅ **Interactive & CLI Modes** - Easy-to-use interface or scriptable commands
✅ **Multiple Providers** - Switch between Hugging Face (free) and Stability AI (limited)

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r tools/requirements.txt
```

**Key dependencies:** `huggingface_hub`, `python-dotenv`, `Pillow`, `PyYAML`, `rembg` (for background removal)

### 2. Get Free API Token

Visit: **https://huggingface.co/settings/tokens**

1. Sign up (no credit card required!)
2. Click "New token" → Select "Read" access
3. Copy your token (starts with `hf_...`)

### 3. Configure API

```bash
# Create .env file
cp .env.example .env
nano .env
```

Add your token:
```
HF_TOKEN=hf_your_token_here
```

### 4. Configure Your Game Settings

```bash
# Copy config template
cp tools/config.yaml.example tools/config.yaml

# Copy style template
cp tools/style_config.yaml.example tools/style_config.yaml
```

### 5. Start Generating!

```bash
python tools/asset_generator.py --interactive
```

---

## API Configuration

API configuration is managed through **two files**: `.env` (secrets) and `config.yaml` (settings).

### `.env` - API Keys (Not tracked in git)

```bash
# Hugging Face Token (FREE, unlimited)
HF_TOKEN=hf_your_token_here

# Stability AI Key (optional, only if using stability provider)
STABILITY_API_KEY=your_stability_key
```

**Security:** The `.env` file is excluded from git to keep your API keys private.

### `config.yaml` - Provider & Generation Settings

```yaml
# Provider selection
provider: "huggingface"  # or "stability"

# Model selection (for Hugging Face)
huggingface_model: "black-forest-labs/FLUX.1-schnell"

# Image dimensions per asset type [width, height]
dimensions:
  npc: [1024, 1024]      # Square for characters
  item: [1024, 1024]     # Square for items
  door: [512, 768]       # Portrait for doors
  room: [1024, 1024]     # Square (or [1920, 1080] for widescreen)

# Background removal per asset type
remove_background:
  npc: true              # Remove background for NPCs (transparent)
  item: true             # Remove background for items (transparent)
  door: false            # Keep background for doors
  room: false            # Keep background for rooms
```

**Override dimensions per-call:**
```bash
# Command-line
python tools/asset_generator.py room "library" library --width 1920 --height 1080

# Interactive mode - you'll be prompted for size
python tools/asset_generator.py --interactive
```

### Provider Comparison

| Feature | Hugging Face (Default) | Stability AI |
|---------|----------------------|--------------|
| **Cost** | FREE | FREE |
| **Limits** | Unlimited* | ~3 images/month |
| **Model** | FLUX.1-schnell | Stable Diffusion 3.5 |
| **Speed** | 20-60 sec | 5-15 sec |
| **Credit Card** | Not required | Not required |
| **Best For** | Everything! | Quick tests only |

*Rate limited but very generous for personal use

**To switch providers:** Edit `config.yaml` and set `provider: "stability"` (requires `STABILITY_API_KEY` in `.env`)

---

## Style Configuration

Your game's visual style is controlled by **`tools/style_config.yaml`**. This is the most important configuration for consistent, high-quality assets.

### Master Style - Applied to ALL Assets

```yaml
master_style:
  art_style: "2D cartoon illustration, hand-drawn style, flat colors, cel-shaded"
  detail_level: "simple, clean lines, not photorealistic, not 3D rendered"
  color_style: "vibrant colors, bold outlines, adventure game aesthetic"
  negative_keywords: "3D render, photorealistic, realistic, cinema4d, unreal engine, 3D animated, CGI, octane render, ray tracing, volumetric lighting, depth of field, Pixar style, Disney 3D"
  additional: "similar to classic point-and-click adventure games like Monkey Island or Day of the Tentacle"
```

**Key fields:**
- **`art_style`** - Define your desired visual style (e.g., "2D cartoon", "pixel art", "watercolor")
- **`negative_keywords`** - **MOST IMPORTANT!** Tells AI what to avoid (e.g., "3D render, CGI, photorealistic")
- **`color_style`** - Color palette guidance (e.g., "vibrant", "muted", "dark and moody")
- **`additional`** - Reference games/artists for style consistency

### Asset-Specific Overrides

Fine-tune each asset type while keeping the master style:

```yaml
npcs:
  style: "full body character sprite, front view, standing pose, 2D game character"
  negative: "side view, multiple poses, action pose, dynamic pose, 3D model"
  additional: "simple character design, clear silhouette, flat shading"

rooms:
  style: "interior background scene, wide angle view, 2D game background art"
  negative: "character in scene, portrait orientation, close-up, 3D environment"
  additional: "atmospheric, detailed environment, clear depth, painted background"

items:
  style: "2D game item icon, single object, centered, clear and recognizable"
  negative: "multiple objects, scene, background elements, text, UI elements, 3D object"
  additional: "inventory item style, easily identifiable, flat icon"

doors:
  style: "front-facing door, architectural element, straight-on view, 2D sprite"
  negative: "perspective view, open door, angled view, 3D model"
  additional: "clear and centered, game asset style, flat rendering"
```

### Quality Boosters & Universal Negatives

```yaml
enhancement:
  style_weight: 0.9
  quality_boosters:
    - "high quality"
    - "clean artwork"
    - "professional game art"
    - "2D illustration"
  universal_negatives:
    - "blurry"
    - "low quality"
    - "distorted"
    - "watermark"
    - "signature"
    - "text"
    - "amateur"
    - "photograph"
```

### Why Negative Keywords Matter

**Problem:** AI models default to popular styles (3D renders, photorealistic) unless explicitly told not to.

**Solution:** Strong negative keywords force the AI to avoid unwanted styles.

**Example - Before:**
```yaml
# Weak negative keywords
negative_keywords: "3D, realistic"
```
Result: Still getting 3D-looking zombies!

**Example - After:**
```yaml
# Strong negative keywords
negative_keywords: "3D render, photorealistic, realistic, cinema4d, unreal engine, 3D animated, CGI, octane render, ray tracing, volumetric lighting, depth of field, Pixar style, Disney 3D"
```
Result: Perfect 2D cartoon zombies! ✅

### Common Style Presets

#### 2D Cartoon (Current Default)
```yaml
art_style: "2D cartoon illustration, hand-drawn style, flat colors, cel-shaded"
negative_keywords: "3D render, photorealistic, CGI, Pixar, Disney 3D"
additional: "similar to Monkey Island, Day of the Tentacle"
```

#### Pixel Art
```yaml
art_style: "pixel art, 16-bit style, retro game sprites"
negative_keywords: "smooth, anti-aliased, high resolution, 3D, realistic"
additional: "similar to classic SNES games"
```

#### Watercolor
```yaml
art_style: "watercolor painting, soft brushstrokes, painted"
negative_keywords: "digital, 3D, photorealistic, vector art"
additional: "hand-painted watercolor illustration"
```

#### Comic Book
```yaml
art_style: "comic book illustration, ink and color, bold linework"
negative_keywords: "3D render, photograph, realistic lighting"
additional: "similar to graphic novels and comics"
```

### Testing Your Style

1. **Generate a test asset:**
   ```bash
   python3 tools/asset_generator.py npc "test character" test
   ```

2. **Check the result:**
   - Is it the right art style?
   - Is it 2D or 3D?
   - Does it match your existing assets?

3. **Adjust if needed:**
   - Edit `style_config.yaml`
   - Add more negative keywords if seeing unwanted styles
   - Strengthen positive descriptions
   - Reference specific games or artists

4. **Regenerate:**
   - Delete the test asset
   - Generate again with updated config

### Troubleshooting Style Issues

**Issue: "Still getting 3D-looking results"**
- ✅ Add more 3D-related terms to `negative_keywords`
- ✅ Make `art_style` description stronger (e.g., "NOT 3D, NOT photorealistic")
- ✅ Reference 2D games in `additional` field

**Issue: "Results vary too much"**
- ✅ Be very specific in style descriptions
- ✅ Use reference games/artists
- ✅ Generate multiple versions and pick the best

**Issue: "Colors are wrong"**
- ✅ Add color guidance to `color_style`:
  ```yaml
  color_style: "vibrant colors, saturated, bold color palette"
  # OR
  color_style: "muted colors, pastel tones, soft palette"
  ```

**For detailed style guide:** See [STYLE_CONFIG_GUIDE.md](../STYLE_CONFIG_GUIDE.md)

---

## Usage

### Interactive Mode (Recommended)

```bash
python tools/asset_generator.py --interactive
```

Prompts you for:
- Asset type
- Description
- Filename
- Image size (shows default, press Enter to accept)
- Background removal (for rooms/doors)

### Command Line

**Basic usage:**
```bash
python tools/asset_generator.py <type> "<description>" <name>
```

**Examples:**
```bash
# NPC with default size (1024x1024)
python tools/asset_generator.py npc "elderly wizard" wizard

# Room with custom widescreen size
python tools/asset_generator.py room "ancient library" library --width 1920 --height 1080

# Item without background removal
python tools/asset_generator.py item "golden key" key --no-bg-removal

# Door with custom portrait size
python tools/asset_generator.py door "wooden door" door --width 512 --height 768
```

### Check Usage Stats

```bash
python tools/asset_generator.py --check-usage
```

Output:
```
Images generated this month: 15 (Hugging Face - unlimited)
```

### List Example Templates

```bash
python tools/asset_generator.py --list-templates
```

Shows example descriptions for NPCs, rooms, items, and doors.

---

## Asset Types

### NPCs (Non-Player Characters)
- **Default Size:** 1024x1024 (square)
- **Background:** Removed (transparent PNG)
- **Style:** Full-body character sprite, front view
- **Location:** `assets/npcs/`

```bash
python tools/asset_generator.py npc "friendly shopkeeper with apron" shopkeeper
python tools/asset_generator.py npc "medieval guard in armor" guard
```

### Rooms (Backgrounds)
- **Default Size:** 1024x1024 (configurable to 1920x1080)
- **Background:** Kept (full scene)
- **Style:** Interior scene, wide angle, atmospheric
- **Location:** `assets/rooms/`

```bash
python tools/asset_generator.py room "cozy tavern with fireplace" tavern
python tools/asset_generator.py room "dark dungeon corridor" dungeon --width 1920 --height 1080
```

### Items (Objects)
- **Default Size:** 1024x1024 (square)
- **Background:** Removed (transparent PNG)
- **Style:** Single object, centered, icon-style
- **Location:** `assets/items/`

```bash
python tools/asset_generator.py item "red potion bottle" potion_red
python tools/asset_generator.py item "ancient scroll" scroll
```

### Doors
- **Default Size:** 512x768 (portrait)
- **Background:** Kept by default
- **Style:** Front-facing, architectural element
- **Location:** `assets/doors/`

```bash
python tools/asset_generator.py door "ornate wooden door" door_ornate
python tools/asset_generator.py door "metal dungeon door" door_dungeon
```

---

## Tips for Best Results

### Writing Good Prompts

✅ **Do:**
- Be specific about appearance and style
- Include key features ("with glasses", "wearing armor", "glowing")
- Describe mood or atmosphere for rooms
- Keep items simple (single object)

❌ **Don't:**
- Use vague descriptions ("a person", "a room")
- Request text or words in images
- Include multiple objects for items
- Ask for specific camera angles (let style config handle it)

### Example Prompts

**NPCs:**
- ✅ "friendly elderly wizard with long white beard and purple robes"
- ✅ "young shopkeeper with brown apron and welcoming smile"
- ❌ "a wizard" (too vague)

**Rooms:**
- ✅ "ancient library with tall bookshelves, candlelight, and mystical atmosphere"
- ✅ "cozy cottage interior with fireplace, wooden furniture, and warm lighting"
- ❌ "a room with books" (too vague)

**Items:**
- ✅ "ornate silver key with emerald gem in the handle"
- ✅ "red potion bottle with glowing magical liquid"
- ❌ "a key and a potion" (multiple objects)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'huggingface_hub'"

```bash
pip install huggingface_hub python-dotenv
```

### "Error: Please set HF_TOKEN in .env file"

1. Create `.env` file: `cp .env.example .env`
2. Get token at: https://huggingface.co/settings/tokens
3. Add to `.env`: `HF_TOKEN=hf_your_token_here`

### "NumPy 2.x detected" Error

Background removal requires NumPy 1.x:

```bash
pip install 'numpy<2'
pip install rembg
```

### Generated Assets Don't Match Style

1. Check `tools/style_config.yaml`
2. Strengthen `negative_keywords` (exclude 3D, CGI, photorealistic)
3. Be more specific in `art_style`
4. Add reference games in `additional`
5. See [STYLE_CONFIG_GUIDE.md](../STYLE_CONFIG_GUIDE.md) for detailed guide

### Background Removal Not Working

1. Check NumPy version: `pip install 'numpy<2'`
2. Install rembg: `pip install rembg`
3. Note: Rooms and doors have background removal disabled by default
4. Use `--no-bg-removal` to skip for any asset type

---

## File Structure

```
tools/
├── asset_generator.py          # Main script
├── config.yaml                 # Your settings (create from .example)
├── config.yaml.example         # Template
├── style_config.yaml           # Your style config (create from .example)
├── style_config.yaml.example   # Template
├── requirements.txt            # Dependencies
├── .usage_tracker.json         # Auto-generated usage tracking
└── README.md                   # This file

.env                            # Your API keys (create from .example)
.env.example                    # Template
```

---

## Advanced: Batch Generation

Generate multiple variations:

```bash
#!/bin/bash
# batch_generate.sh

# Generate 3 zombie variations
python tools/asset_generator.py npc "zombie school kid" zombie_1
python tools/asset_generator.py npc "zombie in suit" zombie_2
python tools/asset_generator.py npc "zombie chef" zombie_3

# Generate room variations
python tools/asset_generator.py room "dark library" library_dark
python tools/asset_generator.py room "bright library" library_bright
```

---

## Related Documentation

- **[STYLE_CONFIG_GUIDE.md](../STYLE_CONFIG_GUIDE.md)** - Comprehensive style configuration guide
- **[QUICKSTART.md](../QUICKSTART.md)** - Quick setup instructions
- **[FREE_ALTERNATIVES.md](../FREE_ALTERNATIVES.md)** - Provider comparison

---

**Happy Asset Creating! 🎨🎮**
