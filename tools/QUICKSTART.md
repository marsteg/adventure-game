# Asset Generator - Quick Start Guide

## Table of Contents
- [Image Generation Setup](#image-generation-setup)
  - [Option A: Local Models (Private, Unlimited)](#option-a-local-models-private-unlimited)
  - [Option B: API Providers (Easy, Fast)](#option-b-api-providers-easy-fast)
- [Audio Generation Setup](#audio-generation-setup)
- [First Steps](#first-steps)
- [Troubleshooting](#troubleshooting)

---

## Image Generation Setup

Choose one or both options:

### Option A: Local Models (Private, Unlimited)

Run AI models directly on your machine - 100% private, no API limits!

**Requirements:**
- 32GB RAM (recommended)
- Apple Silicon (M1/M2/M3) or NVIDIA GPU
- 20-30GB free disk space for models

**1. Install Local Dependencies:**
```bash
pip install 'numpy<2'
pip install torch diffusers transformers accelerate sentencepiece
pip install -r tools/requirements.txt
```

**2. Configure Local Provider:**
```bash
cp tools/config.yaml.example tools/config.yaml
nano tools/config.yaml
```

Set provider to local:
```yaml
provider: "local"

image_settings:
  local:
    active_model: "flux"  # or "sdxl" or "kandinsky"
```

**Available Models:**
- **flux** - Fast (4 steps, ~30-60 sec), 12GB model
- **sdxl** - High quality (25 steps, ~2-3 min), 7GB model
- **kandinsky** - Artistic (25 steps, ~2-3 min), 6GB model

**First-time use**: Models download automatically to `~/.cache/huggingface/` (~6-12GB per model). Subsequent generations use cached models.

---

### Option B: API Providers (Easy, Fast)

Use cloud APIs - fast setup, no hardware requirements!

**1. Install Dependencies:**
```bash
pip install 'numpy<2'
pip install -r tools/requirements.txt
```

**2. Get Free HuggingFace API Token:**
- Go to: https://huggingface.co/settings/tokens
- Click "New token" → Select "Read" access
- Copy your token (no credit card required!)

**3. Configure API Keys:**
```bash
cp .env.example .env
nano .env
```

Add your token:
```bash
HF_TOKEN=hf_your_token_here
```

**4. Select Provider:**
```bash
cp tools/config.yaml.example tools/config.yaml
nano tools/config.yaml
```

```yaml
provider: "huggingface"  # or "stability"
```

---

### Configure Visual Style (Both Options)

```bash
cp tools/style_config.yaml.example tools/style_config.yaml
nano tools/style_config.yaml
```

**Important**: Define your game's art style here! See [STYLE_CONFIG_GUIDE.md](STYLE_CONFIG_GUIDE.md) for details.

---

## Audio Generation Setup

### 1. Choose Your TTS Provider

**Option A: SpeechT5 (Recommended - Easiest)**
- ✅ Lightweight (~500MB)
- ✅ CPU-friendly
- ✅ Good quality
- ✅ Multiple voices available

```bash
pip install torch transformers 'datasets<4.0.0' soundfile sentencepiece
```

**Option B: XTTS-v2 (Voice Cloning)**
- ⭐ Excellent quality
- ⭐ Can clone voices from samples
- ⚠️ Larger download (~2GB)
- ⚠️ GPU recommended
- ⚠️ Requires specific versions: torch<2.6, transformers==4.33.0

```bash
pip install 'torch>=2.0.0,<2.6' TTS
pip install 'transformers==4.33.0'
```

**Option C: KugelAudio (Highest Quality)**
- 🌟 Best quality
- ⚠️ GPU only (~19GB VRAM)
- ⚠️ Manual installation

```bash
git clone https://github.com/Kugelaudio/kugelaudio-open.git
cd kugelaudio-open && uv sync
```

### 2. Select Provider in config.yaml
```yaml
# Choose one:
audio_provider: "speecht5"  # Easiest, CPU-friendly
# audio_provider: "xtts"     # Voice cloning
# audio_provider: "kugelaudio"  # Highest quality
```

### 3. Configure Character Voices (Optional)
```bash
cp tools/voice_config.yaml.example tools/voice_config.yaml
nano tools/voice_config.yaml
```

Customize voices for each character. See [VOICE_CONFIG_GUIDE.md](VOICE_CONFIG_GUIDE.md) for details.

---

## First Steps

### Test Image Generation
```bash
# Interactive mode (recommended for first use)
python tools/asset_generator.py --interactive

# Or command line:
python tools/asset_generator.py npc "test character" test
```

Generated images go to: `assets/npcs/`, `assets/rooms/`, etc.

### Test Audio Generation
```bash
# Generate audio for one character
python tools/asset_generator.py --generate-audio librarian

# Or use interactive mode
python tools/asset_generator.py --interactive
# Select option 7: AUDIO-FILES
```

Generated audio goes to: `assets/sounds/dialogs/`

### Check Usage
```bash
python tools/asset_generator.py --check-usage
```

---

## Troubleshooting

### Image Generation Issues

**"ModuleNotFoundError: No module named 'huggingface_hub'"**
```bash
pip install huggingface_hub python-dotenv
```

**"Error: Please set HF_TOKEN in .env file"**
1. Create `.env`: `cp .env.example .env`
2. Get token: https://huggingface.co/settings/tokens
3. Add to `.env`: `HF_TOKEN=hf_your_token_here`

**"NumPy 2.x detected" Error**
```bash
pip install 'numpy<2'
pip install rembg
```

**"Still getting 3D-looking images"**
- Edit `tools/style_config.yaml`
- Add more keywords to `negative_keywords`:
  ```yaml
  negative_keywords: "3D render, photorealistic, realistic, CGI, octane render, ray tracing"
  ```

### Audio Generation Issues

**"cannot import name 'BeamSearchScorer' from 'transformers'"** (XTTS)
```bash
# Install exact compatible version
pip install 'transformers==4.33.0'
```

**"Weights only load failed"** or **"UnpicklingError"** (XTTS with PyTorch 2.6+)
```bash
# Downgrade torch to 2.5.x
pip install 'torch<2.6' 'torchaudio<2.6'
```

**"Model is multi-speaker but no `speaker` is provided"** (XTTS)
- This is expected - XTTS requires voice samples for cloning
- The tool will automatically download a default speaker on first use
- For better results, configure character voices in `tools/voice_config.yaml`

**"sentencepiece not found"** (SpeechT5)
```bash
pip install sentencepiece
```

**"Dataset scripts are no longer supported"**
```bash
pip install 'datasets<4.0.0'
```

**"CUDA out of memory"** (GPU models)
- Use SpeechT5 instead (CPU-friendly)
- Or reduce batch size
- Or use smaller model

**"Model takes forever to load"**
- First time downloads ~500MB-2GB
- Subsequent runs reuse cached models (fast!)
- Be patient on first run

### General Issues

**"Command not found: python"**
```bash
# Try python3 instead:
python3 tools/asset_generator.py --interactive
```

**"Permission denied"**
```bash
chmod +x tools/asset_generator.py
```

---

## Next Steps

- **[README.md](README.md)** - Complete tool documentation
- **[STYLE_CONFIG_GUIDE.md](STYLE_CONFIG_GUIDE.md)** - Master your art style
- **[VOICE_CONFIG_GUIDE.md](VOICE_CONFIG_GUIDE.md)** - Customize character voices

---

**Ready to create! 🎨🎮🔊**
