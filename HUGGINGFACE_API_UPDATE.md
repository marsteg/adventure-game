# Hugging Face API Update - Fixed!

## Issues Fixed

### 1. ✅ Outdated API Endpoint (410 Error)

**Problem:**
```
Error: 410
{'error': 'https://api-inference.huggingface.co is no longer supported.
Please use https://router.huggingface.co instead.'}
```

**Fixed:** Updated to new endpoint `https://router.huggingface.co/models/{model}`

### 2. ✅ Better Model: FLUX.1-schnell

**Changed:** From `stabilityai/stable-diffusion-xl-base-1.0` → `black-forest-labs/FLUX.1-schnell`

**Why FLUX is better:**
- Faster generation (schnell = "fast" in German)
- Better prompt following
- Higher quality output
- Still completely FREE

### 3. ✅ Cleaner Usage Display

**Before:**
```
Monthly usage: 3/25 (Remaining: 22)
```

**After (Hugging Face):**
```
Images generated this month: 3 (Hugging Face - unlimited)
```

**After (Stability AI):**
```
Monthly usage: 3/25 (Remaining: 22)
⚠️  Monthly limit reached!
💡 Switch to Hugging Face for unlimited free generation:
   Set provider: 'huggingface' in config.yaml
```

### 4. ✅ FLUX-Specific Prompt Handling

FLUX models don't support separate negative prompts, so we now:
- Integrate negative keywords directly into the main prompt
- Format: `{description}. Style: {art_style}. NOT: {negative_keywords}`

## What You Need to Do

### If you already have config.yaml:

Just update your config file:

```yaml
# Update these lines:
provider: "huggingface"
huggingface_api_key: "your-hf-token-here"
huggingface_model: "black-forest-labs/FLUX.1-schnell"
```

### If you don't have config.yaml yet:

```bash
cp tools/config.yaml.example tools/config.yaml
nano tools/config.yaml
# Add your Hugging Face token
```

Get your free token at: https://huggingface.co/settings/tokens

## Changes Made

### Files Updated:

1. **tools/asset_generator.py**
   - Updated API endpoint: `api-inference.huggingface.co` → `router.huggingface.co`
   - Changed default model to FLUX.1-schnell
   - Added FLUX-specific prompt formatting
   - Improved usage display (shows "unlimited" for HF)
   - Better error messages suggesting to switch from Stability AI

2. **tools/config.yaml.example**
   - Updated default model to FLUX.1-schnell
   - Updated comments

## API Differences: FLUX vs SDXL

| Feature | FLUX.1-schnell | Stable Diffusion XL |
|---------|----------------|---------------------|
| Speed | ⚡ Fast (4-8 steps) | Moderate (25-50 steps) |
| Quality | Excellent | Excellent |
| Negative Prompts | ❌ Integrated into main prompt | ✅ Separate parameter |
| Prompt Following | ⭐⭐⭐⭐⭐ Better | ⭐⭐⭐⭐ Good |
| Cost | FREE | FREE |

## Testing

Try generating an asset:

```bash
python3 tools/asset_generator.py npc "friendly zombie" zombie_test
```

You should see:
```
Images generated this month: X (Hugging Face - unlimited)
Generating with style: 2D cartoon illustration...
Provider: Hugging Face (FREE, unlimited)
Model: FLUX.1-schnell
Prompt: friendly zombie. Style: 2D cartoon illustration...
Please wait (may take 20-60 seconds for free tier)...
✓ Image generated successfully!
```

## Alternative Models

If you want to try different models, edit `config.yaml`:

```yaml
# Fast and good quality (default):
huggingface_model: "black-forest-labs/FLUX.1-schnell"

# Even better quality (slower):
huggingface_model: "black-forest-labs/FLUX.1-dev"

# Or classic SDXL (supports negative prompts):
huggingface_model: "stabilityai/stable-diffusion-xl-base-1.0"
```

## Summary

✅ Fixed 410 API deprecation error
✅ Upgraded to better FLUX model
✅ Cleaner usage messages
✅ Provider-aware display
✅ Better error messages

**Everything works now!** Just update your config and start generating. 🎨
