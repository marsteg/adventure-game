# Asset Generator Tool

AI-powered asset generation tool for the Point & Click Adventure Game Engine. Generate high-quality visual assets (images) and audio (character voices) for your game using free AI providers.

## Table of Contents

- [Features](#features)
- [What Can It Generate?](#what-can-it-generate)
- [Quick Start](#quick-start)
- [Usage Overview](#usage-overview)
- [Configuration Guides](#configuration-guides)
- [Examples](#examples)
- [Tips for Best Results](#tips-for-best-results)
- [Troubleshooting](#troubleshooting)

---

## Features

### Image Generation
✅ **FREE Unlimited AI Image Generation** - Uses Hugging Face FLUX.1-schnell model (no credit limits!)
✅ **Centralized Style Control** - Define your game's art style once in `style_config.yaml`
✅ **Negative Prompts** - Exclude unwanted styles (3D, photorealistic, CGI, etc.)
✅ **Configurable Dimensions** - Set default sizes per asset type, override per-generation
✅ **Automatic Background Removal** - Transparent backgrounds for NPCs and items
✅ **Multiple Providers** - Switch between Hugging Face (free) and Stability AI (limited)

### Audio Generation
✅ **Text-to-Speech for NPC Dialogs** - Generate voice audio for all character dialog lines
✅ **Multiple TTS Providers** - SpeechT5 (CPU-friendly), XTTS (voice cloning), or KugelAudio (highest quality)
✅ **Character-Specific Voices** - Configure unique voices for each NPC
✅ **Automatic Batch Generation** - Generate all dialog audio for a character at once
✅ **Voice Cloning Support** - Clone voices from audio samples (XTTS provider)

### General
✅ **Interactive & CLI Modes** - Easy-to-use menu interface or scriptable commands
✅ **Usage Tracking** - Monitor generation counts
✅ **Model Caching** - Fast subsequent generations after initial model download

---

## What Can It Generate?

### Visual Assets (Images)

**NPCs (Characters)**
- Full-body character sprites with transparent backgrounds
- Default: 1024x1024 square images
- Output: `assets/npcs/<name>.png`

**Rooms (Backgrounds)**
- Environment scenes and backgrounds
- Default: 1920x1080 widescreen images (configurable)
- Output: `assets/rooms/<name>.png`

**Items (Objects)**
- Inventory items and objects with transparent backgrounds
- Default: 1024x1024 square images
- Output: `assets/items/<name>.png`

**Doors**
- Door sprites and architectural elements
- Default: 1024x1024 square images
- Output: `assets/doors/<name>.png`

### Audio Assets (Voices)

**NPC Dialog Audio**
- Generates WAV audio files for all dialog lines in a character's YAML file
- Reads from: `assets/dialogs/<character>.yaml`
- Output: `assets/sounds/dialogs/<character>_<dialog-id>.wav` (or uses path from YAML)
- Supports character-specific voice configuration
- Combines array dialogs into single audio file
- Multiple TTS providers for different quality/performance tradeoffs

---

## Quick Start

**Installation and setup instructions:** [QUICKSTART.md](QUICKSTART.md)

The Quick Start guide covers:
- Image generation setup (dependencies, API tokens)
- Audio generation setup (TTS provider installation)
- First test generations
- Common troubleshooting

---

## Usage Overview

### Interactive Mode (Recommended)

Launch the interactive menu to generate assets step-by-step:

```bash
python tools/asset_generator.py --interactive
```

**Menu Options:**
1. **NPC** - Generate character sprites
2. **ROOM** - Generate background scenes
3. **ITEM** - Generate inventory objects
4. **DOOR** - Generate door sprites
5. **DOUBLE-ASSET** - Generate NPCs + rooms together
6. **BATCH-ASSET** - Generate multiple assets from text file
7. **AUDIO-FILES** - Generate dialog audio for a character
8. **EXIT** - Quit

### Command Line Interface

**Image Generation:**
```bash
# Basic syntax
python tools/asset_generator.py <type> "<description>" <name>

# Examples
python tools/asset_generator.py npc "elderly wizard" wizard
python tools/asset_generator.py room "ancient library" library --width 1920 --height 1080
python tools/asset_generator.py item "golden key" key
```

**Audio Generation:**
```bash
# Generate audio for all dialog lines of a character
python tools/asset_generator.py --generate-audio <character_name>

# Example
python tools/asset_generator.py --generate-audio librarian
```

**Utility Commands:**
```bash
# Check usage statistics
python tools/asset_generator.py --check-usage

# List example templates
python tools/asset_generator.py --list-templates
```

---

## Configuration Guides

The tool's behavior is controlled by several configuration files:

### 📘 [QUICKSTART.md](QUICKSTART.md)
Installation and setup guide:
- Installing dependencies (image and audio)
- Getting API tokens
- Choosing TTS providers
- First test generations
- Troubleshooting common issues

### 🎨 [STYLE_CONFIG_GUIDE.md](STYLE_CONFIG_GUIDE.md)
Complete guide to visual style configuration (`style_config.yaml`):
- Master style settings (art style, detail level, colors)
- Asset-specific overrides (NPCs, rooms, items, doors)
- **The power of negative keywords** (most important!)
- Common style presets (2D cartoon, pixel art, watercolor, comic book, etc.)
- Testing and iteration workflow
- Troubleshooting style issues

### 🎭 [VOICE_CONFIG_GUIDE.md](VOICE_CONFIG_GUIDE.md)
Complete guide to character voice configuration (`voice_config.yaml`):
- Provider-specific settings (SpeechT5, XTTS, KugelAudio)
- Character voice mapping
- Finding the right voice for each character
- Voice cloning with XTTS
- Testing and comparing voices
- Pre-configured character voices

---

## Examples

### Image Generation Examples

**Generate an NPC:**
```bash
python tools/asset_generator.py npc "friendly shopkeeper with apron and welcoming smile" shopkeeper
```

**Generate a room with custom dimensions:**
```bash
python tools/asset_generator.py room "cozy tavern with fireplace and wooden tables" tavern --width 1920 --height 1080
```

**Generate an item:**
```bash
python tools/asset_generator.py item "ornate silver key with emerald gem" magic_key
```

**Generate a door:**
```bash
python tools/asset_generator.py door "ancient wooden door with iron hinges" dungeon_door
```

### Audio Generation Examples

**Generate audio for one character:**
```bash
# Interactive mode - select option 7
python tools/asset_generator.py --interactive

# Or command line
python tools/asset_generator.py --generate-audio librarian
```

This will:
1. Read `assets/dialogs/librarian.yaml`
2. Extract all dialog text (description lines, dialog nodes)
3. Combine array dialogs into single audio
4. Generate audio files for each node
5. Save using YAML paths or generate as `librarian_*.wav`

**Example output:**
```
Found 21 dialog nodes with 23 total lines to generate
[1/23] Generating: description-locked
[2/23] Generating: description-unlocked
[3/23] Generating: start
[4/23] Generating: approach
...
✓ Successfully generated 23 audio files
```

---

## Tips for Best Results

### Writing Good Image Prompts

✅ **Do:**
- Be specific about appearance ("elderly wizard with long white beard and purple robes")
- Include key features ("wearing armor", "glowing eyes", "friendly expression")
- Describe mood or atmosphere for rooms ("mystical", "cozy", "ominous")
- Keep items simple - single object only

❌ **Don't:**
- Use vague descriptions ("a person", "a room", "a key")
- Request text or words in images
- Include multiple objects for items
- Worry about art style (handled by `style_config.yaml`)

### Achieving Consistent Visual Style

The **most important** configuration for good results is `style_config.yaml`:

1. **Set your art style** - Define once, applies to all assets
2. **Use strong negative keywords** - Tell AI what to avoid (3D, CGI, photorealistic)
3. **Reference games/artists** - Help AI understand your desired aesthetic
4. **Test and iterate** - Generate test assets, adjust config, regenerate

**See [STYLE_CONFIG_GUIDE.md](STYLE_CONFIG_GUIDE.md) for comprehensive style configuration guide.**

### Customizing Character Voices

For better audio quality, configure character-specific voices in `voice_config.yaml`:

1. **Assign voice IDs** - Each character can have a unique voice (SpeechT5: speaker IDs 0-7325)
2. **Use voice cloning** - Clone voices from audio samples (XTTS provider)
3. **Match character personality** - Authority figures get deeper voices, young characters get lighter voices
4. **Test and compare** - Generate audio, adjust voice settings, regenerate

**See [VOICE_CONFIG_GUIDE.md](VOICE_CONFIG_GUIDE.md) for comprehensive voice configuration guide.**

---

## Troubleshooting

### Image Generation Issues

**"Still getting 3D-looking images"**
- ✅ Strengthen `negative_keywords` in `style_config.yaml`
- ✅ Add: `"3D render, CGI, photorealistic, octane render, ray tracing, volumetric lighting"`
- ✅ See [STYLE_CONFIG_GUIDE.md](STYLE_CONFIG_GUIDE.md) for detailed troubleshooting

**"Results are inconsistent"**
- ✅ Be more specific in `art_style` description
- ✅ Add reference games in `additional` field
- ✅ Generate multiple variations and pick the best

**"NumPy 2.x detected error"**
```bash
pip install 'numpy<2'
pip install rembg
```

### Audio Generation Issues

**"sentencepiece not found" (SpeechT5)**
```bash
pip install sentencepiece
```

**"Dataset scripts are no longer supported"**
```bash
pip install 'datasets<4.0.0'
```

**"Model takes forever to load"**
- First-time download: 500MB-13GB depending on provider
- Subsequent runs reuse cached models (fast!)
- Be patient on first generation

**"Voice doesn't match character"**
- ✅ Edit `voice_config.yaml` to change speaker_id
- ✅ Try different voice IDs (0-7325 for SpeechT5)
- ✅ See [VOICE_CONFIG_GUIDE.md](VOICE_CONFIG_GUIDE.md) for voice selection guide

### General Issues

**"ModuleNotFoundError: No module named 'X'"**
```bash
pip install -r tools/requirements.txt
```

**"Error: Please set HF_TOKEN in .env file"**
1. Copy template: `cp .env.example .env`
2. Get token: https://huggingface.co/settings/tokens
3. Add to `.env`: `HF_TOKEN=hf_your_token_here`

**For more troubleshooting:** See [QUICKSTART.md](QUICKSTART.md)

---

## File Structure

```
tools/
├── asset_generator.py              # Main script
├── config.yaml                     # General settings (create from .example)
├── config.yaml.example             # Template
├── style_config.yaml               # Visual style config (create from .example)
├── style_config.yaml.example       # Template
├── voice_config.yaml               # Character voice config (create from .example)
├── voice_config.yaml.example       # Template
├── requirements.txt                # Dependencies
├── .usage_tracker.json             # Auto-generated usage tracking
├── README.md                       # This file (general overview)
├── QUICKSTART.md                   # Installation and setup guide
├── STYLE_CONFIG_GUIDE.md           # Visual style configuration guide
└── VOICE_CONFIG_GUIDE.md           # Character voice configuration guide

.env                                # Your API keys (create from .example)
.env.example                        # Template
```

---

## Provider Information

### Image Generation Providers

| Feature | Hugging Face (Default) | Stability AI |
|---------|----------------------|--------------|
| **Cost** | FREE | FREE |
| **Limits** | Unlimited* | ~3 images/month |
| **Model** | FLUX.1-schnell | Stable Diffusion 3.5 |
| **Speed** | 20-60 sec | 5-15 sec |
| **Setup** | Easy (API token) | Easy (API token) |

*Rate limited but very generous for personal use

### Audio Generation Providers

| Feature | SpeechT5 | XTTS-v2 | KugelAudio |
|---------|----------|---------|------------|
| **Quality** | Good | Excellent | Highest |
| **Setup** | Easy (pip) | Easy (pip) | Manual (git clone) |
| **Size** | ~500MB | ~2GB | ~13GB |
| **Speed** | Fast | Medium | Slower |
| **CPU Support** | Yes | Limited | No |
| **Voice Cloning** | No | Yes | No |
| **Best For** | Most games | Custom voices | Highest quality |

**Recommendation:** Start with **SpeechT5** for easy setup, switch to **XTTS** if you want voice cloning.

---

## Advanced Features

### Batch Generation

Generate multiple assets from a text file:

1. Create a text file with one asset per line:
   ```
   npc: friendly shopkeeper: shopkeeper
   npc: town guard: guard
   room: marketplace: market
   item: health potion: potion_health
   ```

2. Run batch generation:
   ```bash
   python tools/asset_generator.py --interactive
   # Select option 6: BATCH-ASSET
   ```

### Custom Dimensions Per Asset

Override default dimensions for any generation:

```bash
# Widescreen room
python tools/asset_generator.py room "throne room" throne --width 1920 --height 1080

# Tall portrait door
python tools/asset_generator.py door "castle gate" gate --width 512 --height 768
```

### Background Removal Control

```bash
# Keep background (override default)
python tools/asset_generator.py npc "wizard" wizard --no-bg-removal

# Remove background (override default)
python tools/asset_generator.py room "forest" forest --bg-removal
```

---

## Related Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Installation and setup guide
- **[STYLE_CONFIG_GUIDE.md](STYLE_CONFIG_GUIDE.md)** - Comprehensive visual style configuration
- **[VOICE_CONFIG_GUIDE.md](VOICE_CONFIG_GUIDE.md)** - Comprehensive character voice configuration

---

**Create amazing game assets with AI! 🎨🎮🔊**