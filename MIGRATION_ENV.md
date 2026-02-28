# Migration to .env and Hugging Face SDK

## Changes Made

### 1. ✅ API Keys Moved to .env File
**Before:** API keys in `config.yaml` (tracked in git)
**After:** API keys in `.env` (not tracked in git, more secure)

### 2. ✅ Using Hugging Face Python SDK
**Before:** Direct REST API calls (outdated endpoint)
**After:** Official `huggingface_hub` SDK (current, maintained)

### 3. ✅ Better Security
- API keys no longer in config files
- `.env` added to `.gitignore`
- Environment variables take precedence

## Setup Instructions

### 1. Install New Dependencies
```bash
pip install huggingface_hub python-dotenv
```

### 2. Create .env File
```bash
cp .env.example .env
nano .env
```

Add your Hugging Face token:
```
HF_TOKEN=hf_your_token_here
```

Get token at: https://huggingface.co/settings/tokens

### 3. Update config.yaml
Your `config.yaml` should now look like:
```yaml
provider: "huggingface"
huggingface_model: "black-forest-labs/FLUX.1-schnell"

defaults:
  aspect_ratio: "1:1"
  output_format: "png"
  remove_background_npcs: true
  remove_background_items: true
  remove_background_rooms: false
  remove_background_doors: false
```

**No API keys in config.yaml anymore!** They're in `.env`

### 4. Test It
```bash
python3 tools/asset_generator.py npc "friendly zombie" zombie_test
```

## Files Updated

- ✅ `tools/asset_generator.py` - Uses SDK and loads from .env
- ✅ `tools/requirements.txt` - Added huggingface_hub and python-dotenv
- ✅ `.env.example` - Template for environment variables
- ✅ `.env` - Your actual keys (not tracked in git)
- ✅ `.gitignore` - Excludes .env from git
- ✅ `tools/config.yaml.example` - Removed API keys, points to .env
- ✅ `tools/config.yaml` - Cleaned up (user's file)

## What Happens Now

1. **On startup:** Tool loads `.env` file automatically
2. **HF_TOKEN:** Used for Hugging Face API
3. **STABILITY_API_KEY:** Used if provider is set to "stability"
4. **SDK handles:** Authentication, retries, model loading

## Benefits

✅ **More Secure** - API keys not in git
✅ **Current API** - Using maintained SDK, not deprecated endpoints
✅ **Better Errors** - SDK provides clearer error messages
✅ **Auto-retry** - SDK handles 503 errors automatically
✅ **Type Safety** - SDK returns PIL Image objects

## Troubleshooting

### "ModuleNotFoundError: No module named 'huggingface_hub'"
```bash
pip install huggingface_hub python-dotenv
```

### "Error: Please set HF_TOKEN in .env file"
1. Create `.env` file: `cp .env.example .env`
2. Add your token: `HF_TOKEN=hf_your_token`
3. Get token at: https://huggingface.co/settings/tokens

### "Error: Please set STABILITY_API_KEY in .env file"
Only needed if using Stability AI. For Hugging Face, you only need HF_TOKEN.

## Summary

- API keys → `.env` (secure, not tracked)
- REST calls → SDK (maintained, current)
- Old endpoint → New SDK (works!)
- Everything else → Same (no changes to usage)

Ready to generate! 🎨
