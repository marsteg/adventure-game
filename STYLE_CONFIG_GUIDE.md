# Style Configuration Guide

## Overview

The asset generator now has a powerful centralized style system that lets you control the look of ALL your game assets from a single file: `tools/style_config.yaml`

## Why This Matters

**Before:** Each asset could look different - some 3D rendered, some cartoon, inconsistent styles

**After:** All assets follow your defined style consistently - perfect for a cohesive game look

## The Problem We Solved

### Issue: "My zombie looks like a 3D Pixar character instead of a 2D cartoon!"

This happens because AI models default to popular styles (3D renders, photorealistic, etc.) unless you explicitly tell them not to.

**Solution:** Use negative prompts to exclude unwanted styles!

## How It Works

### 1. Master Style (Applied to Everything)

```yaml
master_style:
  art_style: "2D cartoon illustration, hand-drawn, flat colors"
  detail_level: "simple, clean lines, NOT 3D rendered"
  negative_keywords: "3D render, CGI, photorealistic, Pixar"
```

Every asset gets this style automatically!

### 2. Asset-Specific Overrides

```yaml
npcs:
  style: "full body character sprite, front view"
  negative: "side view, 3D model"
```

Adds NPC-specific requirements while keeping master style.

### 3. Negative Keywords (MOST IMPORTANT!)

Negative keywords tell the AI what to **avoid**:

```yaml
negative_keywords: "3D render, photorealistic, realistic, cinema4d,
  unreal engine, 3D animated, CGI, octane render, ray tracing,
  volumetric lighting, depth of field, Pixar style, Disney 3D"
```

**This is the key to consistent 2D cartoon style!**

## Quick Start

### 1. Copy the Example Config

```bash
cp tools/style_config.yaml.example tools/style_config.yaml
```

### 2. Edit for Your Game

Open `tools/style_config.yaml` and customize:

```yaml
master_style:
  # YOUR game's style
  art_style: "pixel art"
  # OR "watercolor painting"
  # OR "comic book style"
  # OR "minimalist flat design"

  # What to AVOID
  negative_keywords: "3D render, photorealistic, CGI"
```

### 3. Generate Assets

```bash
python3 tools/asset_generator.py npc "zombie" zombie
```

Now it will be YOUR style of zombie, not a 3D one!

## Common Styles

### 2D Cartoon Adventure Game (Like Your Current Assets)

```yaml
master_style:
  art_style: "2D cartoon illustration, hand-drawn style, flat colors, cel-shaded"
  detail_level: "simple, clean lines, not 3D rendered"
  negative_keywords: "3D render, photorealistic, CGI, Pixar, Disney 3D, octane render"
  additional: "similar to Monkey Island, Day of the Tentacle"
```

### Pixel Art

```yaml
master_style:
  art_style: "pixel art, 16-bit style, retro game sprites"
  detail_level: "low resolution, pixelated, chunky pixels"
  negative_keywords: "smooth, anti-aliased, high resolution, 3D, realistic"
  additional: "similar to classic SNES games"
```

### Comic Book Style

```yaml
master_style:
  art_style: "comic book illustration, ink and color, bold linework"
  detail_level: "detailed, dynamic, graphic novel style"
  negative_keywords: "3D render, photograph, realistic lighting"
  additional: "similar to graphic novels and comics"
```

### Watercolor Painting

```yaml
master_style:
  art_style: "watercolor painting, soft brushstrokes, painted"
  detail_level: "artistic, painterly, traditional media"
  negative_keywords: "digital, 3D, photorealistic, vector art"
  additional: "hand-painted watercolor illustration"
```

## Negative Keywords Reference

Use these to exclude specific styles:

### Exclude 3D/CGI Look
```
3D render, CGI, cinema4d, unreal engine, octane render, ray tracing,
volumetric lighting, depth of field, Pixar, Disney 3D, 3D animated
```

### Exclude Realistic/Photo Look
```
photorealistic, realistic, photograph, photo, portrait photography,
DSLR, cinematic lighting, studio lighting
```

### Exclude Modern 3D Game Look
```
unreal engine, unity engine, game engine, next-gen graphics,
PBR materials, ambient occlusion, subsurface scattering
```

### Exclude AI Artifacts
```
blurry, low quality, distorted, watermark, signature, text,
bad anatomy, disfigured, ugly, amateur
```

## Testing Your Style

1. **Generate a test asset:**
   ```bash
   python3 tools/asset_generator.py npc "test character" test
   ```

2. **Check the output:**
   - Is it the right art style?
   - Is it 2D or 3D?
   - Does it match your game?

3. **Adjust if needed:**
   - Edit `style_config.yaml`
   - Add more negative keywords if seeing unwanted styles
   - Strengthen positive descriptions

4. **Regenerate:**
   - Delete the test asset
   - Generate again with updated config

## Advanced Tips

### Make Style Stronger

If results still don't match:

1. **Be MORE specific in art_style:**
   ```yaml
   art_style: "2D hand-drawn cartoon illustration, flat cel-shaded colors,
              bold black outlines, NOT 3D, NOT photorealistic"
   ```

2. **Add MORE negative keywords:**
   ```yaml
   negative_keywords: "3D render, 3D model, 3D graphics, CGI, photorealistic,
                       realistic, octane render, ray tracing, Pixar, Disney 3D,
                       volumetric lighting, depth of field, ambient occlusion"
   ```

3. **Reference specific games/artists:**
   ```yaml
   additional: "in the style of Monkey Island, Day of the Tentacle,
               hand-painted adventure game backgrounds"
   ```

### Per-Asset Fine-Tuning

For specific asset types:

```yaml
npcs:
  style: "2D character sprite, front view, full body"
  negative: "side view, 3D model, realistic proportions"
  additional: "simple cartoon character design"

rooms:
  style: "2D background painting, wide angle"
  negative: "3D environment, realistic lighting, photograph"
  additional: "hand-painted game background"
```

## Troubleshooting

### "Still getting 3D-looking results"

1. Check your negative_keywords - add more 3D-related terms
2. Make art_style description stronger
3. Add "NOT 3D" explicitly in detail_level
4. Reference 2D games in additional field

### "Results look different every time"

This is normal AI variation. To get more consistency:

1. Be very specific in style descriptions
2. Use reference games/artists
3. Increase style_weight (if implemented)
4. Generate multiple versions and pick the best

### "Colors are wrong"

Add color guidance:

```yaml
color_style: "vibrant colors, saturated, bold color palette"
# OR
color_style: "muted colors, pastel tones, soft palette"
```

## Example: Fixing the 3D Zombie

**Before (3D looking zombie):**
- Prompt: "zombie character"
- No negative keywords
- Result: 3D rendered zombie

**After (2D cartoon zombie):**
```yaml
master_style:
  art_style: "2D cartoon illustration, flat colors, cel-shaded"
  negative_keywords: "3D render, CGI, photorealistic, Pixar style"

npcs:
  style: "2D character sprite, cartoon style"
  negative: "3D model, realistic"
```

- Prompt built: "zombie character, 2D character sprite, 2D cartoon illustration, flat colors..."
- Negative: "3D render, CGI, photorealistic, Pixar style, 3D model, realistic..."
- Result: ✅ Perfect 2D cartoon zombie!

## Summary

**The secret to consistent style:**
1. Define your master style once in `style_config.yaml`
2. Use strong negative keywords to exclude unwanted styles
3. Be specific about what you want AND what you don't want
4. Reference existing games/art styles
5. Test and refine

Now all your assets will have a consistent, professional look! 🎨
