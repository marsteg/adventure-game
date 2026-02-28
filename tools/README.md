# Asset Generator Tool

AI-powered asset generation tool for the Point & Click Adventure Game Engine. Generate NPCs, rooms, items, and doors using Stability AI's free tier.

## Features

✅ **Free AI Image Generation** - Uses Stability AI free tier (25 images/month)
✅ **Asset Type Templates** - Pre-configured prompts for NPCs, rooms, items, doors
✅ **Automatic Background Removal** - Removes backgrounds for NPCs and items
✅ **Style Consistency** - Maintains your game's art style
✅ **Usage Tracking** - Tracks monthly API usage
✅ **Interactive Mode** - Easy-to-use CLI interface
✅ **Batch Generation** - Generate multiple assets quickly

## Installation

### 1. Install Dependencies

```bash
pip install -r tools/requirements.txt
```

**Dependencies:**
- `requests` - API communication
- `PyYAML` - Configuration files
- `Pillow` - Image processing
- `rembg` - Background removal (optional but recommended)

### 2. Get Your Free API Key

1. Go to [Stability AI Platform](https://platform.stability.ai/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key
5. Free tier includes **25 image generations per month**

### 3. Configure the Tool

```bash
# Copy the example config
cp tools/config.yaml.example tools/config.yaml

# Edit config.yaml and add your API key
# Replace 'your-api-key-here' with your actual API key
```

## Usage

### Quick Start - Interactive Mode

The easiest way to generate assets:

```bash
python tools/asset_generator.py --interactive
```

This will guide you through generating assets step-by-step.

### Command Line Usage

#### Generate an NPC

```bash
python tools/asset_generator.py npc "friendly shopkeeper with apron" shopkeeper
```

#### Generate a Room

```bash
python tools/asset_generator.py room "dark mysterious library with ancient books" library_dark
```

#### Generate an Item

```bash
python tools/asset_generator.py item "golden ornate key with ruby" key_ornate
```

#### Generate a Door

```bash
python tools/asset_generator.py door "heavy wooden door with iron lock" door_castle
```

### Advanced Options

#### Disable Background Removal

```bash
python tools/asset_generator.py npc "wizard character" wizard --no-bg-removal
```

#### Check Usage

```bash
python tools/asset_generator.py --check-usage
```

Output:
```
Monthly usage: 5/25 (Remaining: 20)
```

#### List Available Templates

```bash
python tools/asset_generator.py --list-templates
```

## Asset Types

### NPCs (Non-Player Characters)

- **Style**: Full-body character illustrations, cartoon style
- **Background**: Automatically removed (transparent)
- **Size**: 1024x1024 PNG
- **Location**: `assets/npcs/`

**Examples:**
```bash
python tools/asset_generator.py npc "elderly professor with glasses and lab coat" professor
python tools/asset_generator.py npc "medieval guard in armor" guard
python tools/asset_generator.py npc "friendly tavern keeper" tavern_keeper
```

### Rooms (Backgrounds)

- **Style**: Detailed interior backgrounds, atmospheric
- **Background**: Kept (full scene)
- **Size**: 1024x1024 PNG
- **Location**: `assets/rooms/`

**Examples:**
```bash
python tools/asset_generator.py room "grand castle throne room with red carpet" throne_room
python tools/asset_generator.py room "cozy cottage interior with fireplace" cottage
python tools/asset_generator.py room "mysterious cave with glowing crystals" crystal_cave
```

### Items (Objects)

- **Style**: Clear icon-style illustrations, single object
- **Background**: Automatically removed (transparent)
- **Size**: 1024x1024 PNG
- **Location**: `assets/items/`

**Examples:**
```bash
python tools/asset_generator.py item "ancient scroll with red seal" scroll_ancient
python tools/asset_generator.py item "blue glowing magical potion" potion_magic
python tools/asset_generator.py item "rusty old key" key_rusty
```

### Doors

- **Style**: Front-facing door illustrations
- **Background**: Usually kept, can be removed
- **Size**: 1024x1024 PNG
- **Location**: `assets/doors/`

**Examples:**
```bash
python tools/asset_generator.py door "ornate wooden door with brass handle" door_ornate
python tools/asset_generator.py door "metal dungeon door with bars" door_dungeon
```

## Prompt Templates

The tool includes pre-configured templates for common asset types. Each template has:
- **Style guide** - Consistent art direction
- **Templates** - Common asset variations
- **Negative prompts** - What to avoid

Templates are located in `tools/prompts/`:
- `npc_prompts.yaml` - Character templates
- `room_prompts.yaml` - Room/background templates
- `item_prompts.yaml` - Item/object templates
- `door_prompts.yaml` - Door templates

You can edit these files to customize the style for your game!

## Tips for Best Results

### Writing Good Prompts

✅ **Do:**
- Be specific about what you want
- Include style keywords (e.g., "cartoon", "detailed", "ornate")
- Describe key features (e.g., "with glasses", "wearing armor")
- Keep it concise but descriptive

❌ **Don't:**
- Use vague descriptions (e.g., "a person")
- Include multiple objects in item prompts
- Ask for text or words in the image
- Request complex scenes for items

### Examples of Good Prompts

**NPCs:**
- "friendly elderly wizard with long white beard and purple robes"
- "young shopkeeper with brown apron and welcoming smile"
- "mysterious hooded figure in dark cloak"

**Rooms:**
- "ancient library with tall bookshelves and candlelight"
- "royal bedroom with four-poster bed and red curtains"
- "dungeon corridor with stone walls and torches"

**Items:**
- "ornate silver key with emerald gem in handle"
- "red potion bottle with glowing liquid"
- "leather-bound book with golden clasp"

### Style Consistency

The tool automatically adds style guidelines based on your existing assets. The prompts are configured to match the cartoon/illustrated style seen in your game.

If generated assets don't match your style:
1. Check the `style_guide` in prompt templates
2. Adjust the style descriptions
3. Add more specific style keywords

## Usage Limits & Costs

### Free Tier (Stability AI)

- **Cost**: FREE
- **Limit**: 25 images per month
- **Quality**: High quality, 1024x1024
- **Commercial use**: Allowed

### Tracking Usage

The tool automatically tracks your usage in `tools/.usage_tracker.json`:

```json
{
  "month": "2026-02",
  "count": 5
}
```

This resets automatically each month.

### If You Hit the Limit

Options:
1. **Wait until next month** (free tier resets monthly)
2. **Upgrade to paid plan** (Stability AI offers paid tiers)
3. **Use alternative service** (e.g., Replicate, Hugging Face)

## Troubleshooting

### "PIL not available"

```bash
pip install Pillow
```

### "rembg not available"

Background removal won't work without this:

```bash
pip install rembg
```

### "Config file not found"

Make sure you've created `tools/config.yaml`:

```bash
cp tools/config.yaml.example tools/config.yaml
```

### "Please set your Stability AI API key"

Edit `tools/config.yaml` and replace `your-api-key-here` with your actual API key.

### Generated Image Doesn't Match Style

1. Edit the prompt templates in `tools/prompts/`
2. Adjust the `style_guide` field
3. Add more specific style keywords to match your game

### Background Not Removed

The tool works perfectly without background removal! It will generate images with backgrounds included.

**To enable background removal (optional):**

1. Fix NumPy compatibility:
   ```bash
   pip install 'numpy<2'
   ```

2. Install rembg:
   ```bash
   pip install rembg
   ```

3. For rooms/doors, background removal is disabled by default (you want the background!)
4. Use `--no-bg-removal` flag to disable for NPCs/items if needed

**Note:** Background removal is only useful for NPCs and items. The tool generates images either way!

## File Structure

```
tools/
├── asset_generator.py          # Main script
├── config.yaml                 # Your API configuration (create this!)
├── config.yaml.example         # Template configuration
├── requirements.txt            # Python dependencies
├── .usage_tracker.json         # Usage tracking (auto-generated)
├── prompts/
│   ├── npc_prompts.yaml       # NPC templates
│   ├── room_prompts.yaml      # Room templates
│   ├── item_prompts.yaml      # Item templates
│   └── door_prompts.yaml      # Door templates
└── README.md                   # This file
```

## Examples Gallery

### NPCs Generated
- `janitor.png` - Friendly janitor with mop
- `wizard.png` - Magical wizard character
- `librarian.png` - Scholarly librarian
- `villager_male.png` - Common villager

### Rooms Generated
- `Library.png` - Dark mysterious library
- `MainHall.png` - Grand entrance hall
- `StorageRoom.png` - Storage area

### Items Generated
- `key_gold.png` - Golden ornate key
- `potion_blue.png` - Blue magical potion
- `ancient_scroll.png` - Old parchment scroll

## Advanced: Batch Generation

Want to generate multiple variations? Create a script:

```bash
#!/bin/bash
# generate_npcs.sh

python tools/asset_generator.py npc "friendly merchant" merchant_1
python tools/asset_generator.py npc "friendly merchant" merchant_2
python tools/asset_generator.py npc "friendly merchant" merchant_3
```

## API Reference

### Stability AI Endpoints

The tool uses Stability AI's v2beta API:
- Endpoint: `https://api.stability.ai/v2beta/stable-image/generate/sd3`
- Model: Stable Diffusion 3.5 Large
- Format: PNG, 1024x1024, aspect ratio 1:1

### Configuration Options

Edit `tools/config.yaml`:

```yaml
stability_api_key: "your-key"
monthly_limit: 25
model: "sd3"
defaults:
  aspect_ratio: "1:1"
  output_format: "png"
  remove_background_npcs: true
  remove_background_items: true
  remove_background_rooms: false
  remove_background_doors: false
```

## Contributing

Found a bug or want to improve the tool? Contributions welcome!

## License

This tool is part of the Point & Click Adventure Game Engine project.

## Support

- **Stability AI Docs**: https://platform.stability.ai/docs
- **Get API Key**: https://platform.stability.ai/account/keys
- **Game Engine Docs**: See main README.md

---

**Happy Asset Creating! 🎨🎮**
