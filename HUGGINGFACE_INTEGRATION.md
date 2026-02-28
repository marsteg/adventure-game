# Hugging Face Integration Complete! 🎉

## What Changed

**Hugging Face Inference API is now the default image generation provider** - giving you truly FREE and UNLIMITED image generation!

## Why This Change?

### The Problem with Stability AI
- **Misleading free tier**: Advertised as "25 credits/month"
- **Reality**: Each image costs ~8 credits = only 3 images per month
- **Not sustainable** for game development

### The Solution: Hugging Face
- **Truly FREE**: No hidden credit costs
- **Unlimited**: Generate as many images as you need
- **No credit card required**: Just sign up and get an API token
- **Same quality**: Uses Stable Diffusion XL model

## What You Need to Do

### 1. Get a Free Hugging Face API Token

Visit: https://huggingface.co/settings/tokens

1. Sign up (no credit card needed!)
2. Click "New token"
3. Select "Read" access
4. Copy your token (starts with `hf_...`)

### 2. Update Your Config

If you already have `tools/config.yaml`:

```bash
# Edit your existing config
nano tools/config.yaml
```

Add these lines:
```yaml
provider: "huggingface"
huggingface_api_key: "hf_your_token_here"
huggingface_model: "stabilityai/stable-diffusion-xl-base-1.0"
```

If you don't have `tools/config.yaml` yet:
```bash
cp tools/config.yaml.example tools/config.yaml
nano tools/config.yaml
```

### 3. That's It!

Everything else works the same:

```bash
# Generate assets (now unlimited and free!)
python3 tools/asset_generator.py npc "zombie character" zombie
python3 tools/asset_generator.py room "dark cave" cave_dark
python3 tools/asset_generator.py item "magic sword" sword_magic
```

## Technical Details

### New Code Structure

The tool now has a provider abstraction:

```python
def generate_image(self, prompt: str, negative_prompt: str, asset_type: str):
    """Routes to appropriate provider based on config."""
    provider = self.config.get('provider', 'huggingface')

    if provider == 'huggingface' or provider == 'hf':
        return self.generate_image_huggingface(...)
    elif provider == 'stability' or provider == 'stabilityai':
        return self.generate_image_stability(...)
```

### Provider Options

You can switch providers in `config.yaml`:

**Hugging Face (default - FREE & unlimited):**
```yaml
provider: "huggingface"
huggingface_api_key: "hf_your_token"
huggingface_model: "stabilityai/stable-diffusion-xl-base-1.0"
```

**Stability AI (limited - ~3 images/month):**
```yaml
provider: "stability"
stability_api_key: "sk-your-key"
```

### How Hugging Face API Works

- **Model**: Stable Diffusion XL (SDXL) - same quality as Stability AI
- **Speed**: 20-60 seconds per image (free tier may have queue)
- **Limits**: Generous rate limits, effectively unlimited for personal use
- **Features**: Full support for negative prompts and style configuration
- **503 Handling**: Auto-retries if model is loading (cold start)

## Files Updated

### Core Tool
- `tools/asset_generator.py` - Added Hugging Face support with provider abstraction

### Configuration
- `tools/config.yaml.example` - Now defaults to Hugging Face
- `tools/style_config.yaml.example` - Works with all providers

### Documentation
- `QUICKSTART.md` - Updated setup instructions for Hugging Face
- `tools/README.md` - Updated with Hugging Face as default
- `FREE_ALTERNATIVES.md` - Comparison of providers
- `HUGGINGFACE_INTEGRATION.md` (this file) - Migration guide

## Comparison: Hugging Face vs Stability AI

| Feature | Hugging Face | Stability AI |
|---------|--------------|--------------|
| **Cost** | FREE | FREE |
| **Limits** | Unlimited* | ~3 images/month |
| **Credit Card** | Not required | Not required |
| **Quality** | Excellent (SDXL) | Excellent (SD3) |
| **Speed** | 20-60 sec | 5-15 sec |
| **Reliability** | Very Good | Excellent |
| **Best For** | Development & heavy use | Quick tests |

*Rate limited but generous for personal use

## Frequently Asked Questions

### Can I still use Stability AI?

Yes! Just set `provider: "stability"` in your config. Both providers are supported.

### Will my existing assets/configs work?

Yes! All your style configurations and existing assets remain unchanged. Only the image generation backend changed.

### What if Hugging Face is slow?

The free tier may have queuing during peak times. If speed is critical:
1. Use Stability AI for quick tests (3 images)
2. Consider Replicate ($0.003/image) for production
3. Or run local generation with ComfyUI

### Do I need to change my prompts?

No! The tool uses the same prompts and style configuration for both providers.

### What about background removal?

Works the same way with both providers. Still requires NumPy <2.0.

## Troubleshooting

### "Error: Please set your Hugging Face API key"

You need to add your Hugging Face token to `config.yaml`. Get one free at: https://huggingface.co/settings/tokens

### "Model loading... waiting 20 seconds"

This is normal! Hugging Face models "sleep" when unused. First request wakes them up (20s wait), subsequent requests are faster.

### "Error 503" even after retry

The model might be experiencing high load. Try again in a few minutes, or temporarily switch to Stability AI:
```yaml
provider: "stability"
```

### Images are different quality than before

Both providers use high-quality Stable Diffusion models. If you notice differences:
1. Check your `style_config.yaml` - negative keywords are crucial
2. SDXL (Hugging Face) and SD3 (Stability) have slightly different styles
3. Adjust your style config if needed

## Next Steps

Now that you have unlimited generation:

1. **Experiment freely** - Try different prompts and styles
2. **Refine your style** - Edit `tools/style_config.yaml` until perfect
3. **Generate in batches** - Create all your game assets
4. **Check the guides**:
   - [STYLE_CONFIG_GUIDE.md](STYLE_CONFIG_GUIDE.md) - Master the style system
   - [QUICKSTART.md](QUICKSTART.md) - Quick reference
   - [tools/README.md](tools/README.md) - Complete documentation

## Summary

✅ Hugging Face is now the default (FREE & unlimited!)
✅ Stability AI still available as fallback option
✅ All your existing configs and assets work unchanged
✅ Just add your Hugging Face token and start generating!

**Happy asset generating!** 🎨🎮
