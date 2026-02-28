# Asset Generator Worktree

This worktree contains the new AI-powered asset generation tool for creating game assets (NPCs, rooms, items, doors).

## What's New

- **tools/asset_generator.py** - Main CLI tool for generating assets
- **tools/prompts/** - Pre-configured prompt templates for each asset type
- **tools/config.yaml.example** - Configuration template
- **tools/requirements.txt** - Python dependencies
- **tools/README.md** - Comprehensive documentation

## Quick Start

1. Install dependencies: `pip install -r tools/requirements.txt`
2. Get free API key from https://platform.stability.ai/
3. Copy config: `cp tools/config.yaml.example tools/config.yaml`
4. Add your API key to `tools/config.yaml`
5. Run: `python tools/asset_generator.py --interactive`

## Features

- ✅ Free AI image generation (25/month with Stability AI)
- ✅ Automatic background removal for NPCs/items
- ✅ Style-consistent with existing assets
- ✅ Usage tracking to stay within limits
- ✅ Interactive and CLI modes
- ✅ Pre-built prompt templates

See `tools/README.md` for full documentation.
