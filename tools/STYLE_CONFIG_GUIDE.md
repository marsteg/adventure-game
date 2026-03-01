# Style Configuration Guide

Complete guide to mastering your game's visual style through `style_config.yaml`.

## Table of Contents
- [Overview](#overview)
- [Configuration Structure](#configuration-structure)
- [Master Style Settings](#master-style-settings)
- [Asset-Specific Overrides](#asset-specific-overrides)
- [The Power of Negative Keywords](#the-power-of-negative-keywords)
- [Common Style Presets](#common-style-presets)
- [Testing and Iteration](#testing-and-iteration)
- [Troubleshooting](#troubleshooting)

---

## Overview

The style configuration system ensures **consistent, high-quality visuals** across all your game assets. It works by:

1. **Master Style** - Applied to every asset
2. **Asset Overrides** - Fine-tune specific asset types (NPCs, rooms, items, doors)
3. **Negative Keywords** - Tell AI what to avoid (most important!)
4. **Quality Boosters** - Enhance output quality

**File Location**: `tools/style_config.yaml`

---

## Configuration Structure

```yaml
master_style:          # Applied to ALL assets
  art_style: "..."
  detail_level: "..."
  color_style: "..."
  negative_keywords: "..."
  additional: "..."

npcs:                  # NPC-specific style
  style: "..."
  negative: "..."
  additional: "..."

rooms:                 # Room-specific style
  style: "..."
  negative: "..."
  additional: "..."

items:                 # Item-specific style
  style: "..."
  negative: "..."
  additional: "..."

doors:                 # Door-specific style
  style: "..."
  negative: "..."
  additional: "..."

enhancement:           # Quality settings
  quality_boosters: [...]
  universal_negatives: [...]
```

---

## Master Style Settings

### art_style

**Purpose**: Define your game's primary visual style

**Examples**:
```yaml
# 2D Cartoon
art_style: "2D cartoon illustration, hand-drawn style, flat colors, cel-shaded"

# Pixel Art
art_style: "pixel art, 16-bit style, retro game sprites, pixelated"

# Watercolor
art_style: "watercolor painting, soft brushstrokes, painted illustration"

# Comic Book
art_style: "comic book illustration, ink and color, bold linework"

# Dark Fantasy
art_style: "dark fantasy illustration, gothic art style, dramatic shadows"
```

### detail_level

**Purpose**: Control complexity and rendering style

**Examples**:
```yaml
# Simple/Clean
detail_level: "simple, clean lines, not photorealistic, not 3D rendered"

# Detailed
detail_level: "highly detailed, intricate artwork, rich textures"

# Minimalist
detail_level: "minimalist, simple shapes, clean design"
```

### color_style

**Purpose**: Guide color palette and mood

**Examples**:
```yaml
# Vibrant
color_style: "vibrant colors, bold outlines, adventure game aesthetic"

# Muted/Pastel
color_style: "muted colors, pastel tones, soft color palette"

# Dark/Moody
color_style: "dark colors, moody atmosphere, desaturated palette"

# High Contrast
color_style: "high contrast, bold colors, striking color scheme"
```

### negative_keywords

**Purpose**: **MOST IMPORTANT!** Tell AI what to avoid

**Why It Matters**:
- AI defaults to popular styles (3D, photorealistic)
- Strong negatives force different styles
- More keywords = better results

**Essential Keywords for 2D Games**:
```yaml
negative_keywords: "3D render, photorealistic, realistic, cinema4d, unreal engine, 3D animated, CGI, octane render, ray tracing, volumetric lighting, depth of field, Pixar style, Disney 3D, blender, maya, 3D model"
```

**For Pixel Art**:
```yaml
negative_keywords: "smooth, anti-aliased, high resolution, 3D, realistic, blurry, photorealistic"
```

**For Hand-Drawn**:
```yaml
negative_keywords: "digital art, 3D, photorealistic, CGI, computer generated, vector art, clean lines"
```

### additional

**Purpose**: Reference styles, artists, or games for consistency

**Examples**:
```yaml
# Reference Games
additional: "similar to classic point-and-click adventure games like Monkey Island or Day of the Tentacle"

# Reference Art Style
additional: "Studio Ghibli inspired, hand-painted animation style"

# Reference Artists
additional: "in the style of adventure game concept art"

# Reference Era
additional: "1990s adventure game aesthetic, classic LucasArts style"
```

---

## Asset-Specific Overrides

### NPCs (Characters)

**Focus**: Full-body character sprites, clear silhouette

```yaml
npcs:
  style: "full body character sprite, front view, standing pose, 2D game character"
  negative: "side view, multiple poses, action pose, dynamic pose, 3D model, cropped"
  additional: "simple character design, clear silhouette, flat shading"
```

**Tips**:
- Specify "full body" to avoid crops
- "Front view" for consistency
- "Standing pose" for neutral stance

### Rooms (Backgrounds)

**Focus**: Wide environment scenes, atmospheric

```yaml
rooms:
  style: "interior background scene, wide angle view, 2D game background art"
  negative: "character in scene, portrait orientation, close-up, 3D environment, outdoor"
  additional: "atmospheric, detailed environment, clear depth, painted background"
```

**Tips**:
- "Wide angle" for full room view
- "No characters" to avoid NPCs in backgrounds
- Specify "interior" or "exterior" as needed

### Items (Inventory Objects)

**Focus**: Single centered objects, clear and recognizable

```yaml
items:
  style: "2D game item icon, single object, centered, clear and recognizable"
  negative: "multiple objects, scene, background elements, text, UI elements, 3D object"
  additional: "inventory item style, easily identifiable, flat icon"
```

**Tips**:
- "Single object" prevents multiple items
- "Centered" for clean composition
- "No text" avoids words in images

### Doors

**Focus**: Front-facing, architectural, clear entry point

```yaml
doors:
  style: "front-facing door, architectural element, straight-on view, 2D sprite"
  negative: "perspective view, open door, angled view, 3D model"
  additional: "clear and centered, game asset style, flat rendering"
```

**Tips**:
- "Straight-on view" for consistency
- "Closed door" if you want default closed state
- Can specify door type: "wooden", "metal", "ornate"

---

## The Power of Negative Keywords

### Why They're Critical

**Without strong negatives**:
```yaml
negative_keywords: "3D, realistic"
```
**Result**: ❌ Still getting 3D-looking renders

**With strong negatives**:
```yaml
negative_keywords: "3D render, photorealistic, realistic, cinema4d, unreal engine, 3D animated, CGI, octane render, ray tracing, volumetric lighting, depth of field, Pixar style, Disney 3D"
```
**Result**: ✅ Perfect 2D cartoon style!

### Building Your Negative List

**Start with basics**:
```yaml
"3D, realistic, photorealistic"
```

**Add rendering terms**:
```yaml
"3D render, CGI, octane render, ray tracing, unreal engine"
```

**Add specific styles to avoid**:
```yaml
"Pixar, Disney 3D, Blender, Maya, Cinema4D"
```

**Add technical terms**:
```yaml
"volumetric lighting, depth of field, subsurface scattering, ambient occlusion"
```

**Final combined list**:
```yaml
negative_keywords: "3D render, photorealistic, realistic, cinema4d, unreal engine, 3D animated, CGI, octane render, ray tracing, volumetric lighting, depth of field, Pixar style, Disney 3D, blender, maya, 3D model, subsurface scattering, ambient occlusion"
```

### Common Negative Keywords by Style

**2D Cartoon**:
```
3D render, photorealistic, realistic, CGI, Pixar, Disney 3D, ray tracing
```

**Pixel Art**:
```
smooth, anti-aliased, high resolution, 3D, realistic, blurry, HD
```

**Hand-Drawn/Watercolor**:
```
digital, 3D, photorealistic, CGI, computer generated, perfect lines
```

**Comic Book**:
```
3D, photorealistic, painterly, soft edges, blurry, realistic lighting
```

---

## Common Style Presets

### 1. 2D Cartoon (LucasArts Style)

```yaml
master_style:
  art_style: "2D cartoon illustration, hand-drawn style, flat colors, cel-shaded"
  detail_level: "simple, clean lines, not photorealistic, not 3D rendered"
  color_style: "vibrant colors, bold outlines, adventure game aesthetic"
  negative_keywords: "3D render, photorealistic, realistic, cinema4d, unreal engine, 3D animated, CGI, octane render, ray tracing, volumetric lighting, depth of field, Pixar style, Disney 3D"
  additional: "similar to classic point-and-click adventure games like Monkey Island or Day of the Tentacle"
```

### 2. Pixel Art (Retro)

```yaml
master_style:
  art_style: "pixel art, 16-bit style, retro game sprites, pixelated, 8-bit aesthetic"
  detail_level: "simple pixel art, limited color palette, clear pixels"
  color_style: "retro gaming colors, vibrant 16-bit palette"
  negative_keywords: "smooth, anti-aliased, high resolution, 3D, realistic, blurry, HD, photorealistic, detailed textures"
  additional: "similar to classic SNES or Sega Genesis games, 1990s pixel art style"
```

### 3. Watercolor Fantasy

```yaml
master_style:
  art_style: "watercolor painting, soft brushstrokes, painted illustration, traditional media"
  detail_level: "painterly, artistic, hand-painted feel, organic textures"
  color_style: "soft muted colors, watercolor palette, gentle color bleeding"
  negative_keywords: "digital, 3D, photorealistic, CGI, vector art, clean lines, sharp edges, computer generated"
  additional: "hand-painted watercolor illustration, traditional fantasy art"
```

### 4. Dark Gothic Horror

```yaml
master_style:
  art_style: "dark fantasy illustration, gothic art style, dramatic shadows, horror aesthetic"
  detail_level: "detailed, atmospheric, intricate linework"
  color_style: "dark colors, moody atmosphere, desaturated palette, dramatic lighting"
  negative_keywords: "bright, colorful, cheerful, cartoon, cute, 3D render, photorealistic"
  additional: "gothic horror game aesthetic, dark fantasy art"
```

### 5. Comic Book / Graphic Novel

```yaml
master_style:
  art_style: "comic book illustration, ink and color, bold linework, graphic novel style"
  detail_level: "clean strong lines, cel-shaded, flat colors with shadows"
  color_style: "bold colors, high contrast, comic book color palette"
  negative_keywords: "3D render, photograph, realistic lighting, soft edges, blurry, painterly"
  additional: "similar to graphic novels and superhero comics, Mike Mignola style"
```

### 6. Minimalist Modern

```yaml
master_style:
  art_style: "minimalist illustration, simple shapes, clean design, modern flat art"
  detail_level: "minimalist, simple geometric shapes, clean lines"
  color_style: "limited color palette, flat colors, modern aesthetic"
  negative_keywords: "detailed, complex, realistic, 3D, textured, busy, ornate"
  additional: "modern flat design, minimalist game art"
```

---

## Testing and Iteration

### Step 1: Generate Test Asset

```bash
python tools/asset_generator.py npc "test character for style" test_character
```

### Step 2: Evaluate Result

Check for:
- ✅ Correct art style (2D vs 3D)
- ✅ Appropriate detail level
- ✅ Right color palette
- ✅ No unwanted elements
- ✅ Consistency with vision

### Step 3: Adjust Configuration

**If too 3D-looking**:
```yaml
# Add more negative keywords
negative_keywords: "3D render, CGI, realistic, Pixar, octane render, ray tracing, volumetric lighting, depth of field"
```

**If wrong style**:
```yaml
# Be more specific in art_style
art_style: "2D hand-drawn cartoon, NOT 3D, NOT photorealistic, flat colors"
```

**If too detailed/complex**:
```yaml
# Simplify detail level
detail_level: "simple, clean, minimalist, not overly detailed"
```

**If colors are wrong**:
```yaml
# Specify exact palette
color_style: "vibrant saturated colors, bold primary colors, no muted tones"
```

### Step 4: Regenerate

```bash
# Delete old test
rm assets/npcs/test_character.png

# Generate with new settings
python tools/asset_generator.py npc "test character for style" test_character
```

### Step 5: Compare and Refine

Keep iterating until you get the style you want!

---

## Troubleshooting

### Problem: Still Getting 3D Renders

**Solution 1**: Strengthen negative keywords
```yaml
negative_keywords: "3D render, photorealistic, realistic, cinema4d, unreal engine, 3D animated, CGI, octane render, ray tracing, volumetric lighting, depth of field, Pixar style, Disney 3D, blender, maya, 3D model, ambient occlusion, subsurface scattering"
```

**Solution 2**: Add "NOT 3D" to art_style
```yaml
art_style: "2D cartoon illustration, hand-drawn, flat colors, NOT 3D, NOT photorealistic"
```

**Solution 3**: Reference 2D games explicitly
```yaml
additional: "similar to 2D adventure games like Monkey Island, classic LucasArts style, 1990s point-and-click aesthetic"
```

### Problem: Inconsistent Results

**Solution 1**: Be more specific
```yaml
# Vague
art_style: "cartoon"

# Specific
art_style: "2D hand-drawn cartoon with flat colors and cel-shaded style"
```

**Solution 2**: Add reference games/artists
```yaml
additional: "in the style of Day of the Tentacle, Grim Fandango, or Broken Sword"
```

**Solution 3**: Generate multiple versions
```bash
# Generate 3 variations and pick best
python tools/asset_generator.py npc "character" char_v1
python tools/asset_generator.py npc "character" char_v2
python tools/asset_generator.py npc "character" char_v3
```

### Problem: Wrong Colors

**Solution 1**: Be explicit about colors
```yaml
color_style: "vibrant saturated colors, high contrast, bold color palette, NO muted tones, NO desaturated colors"
```

**Solution 2**: Specify mood
```yaml
# For bright game
color_style: "bright cheerful colors, colorful, vibrant"

# For dark game
color_style: "dark moody colors, low saturation, muted palette"
```

### Problem: Characters Have Multiple Poses

**Solution**: Specify in NPC overrides
```yaml
npcs:
  style: "full body character sprite, front view, SINGLE standing pose, static pose"
  negative: "multiple poses, action pose, dynamic pose, character sheet, turnaround, poses, animation frames"
```

### Problem: Items Have Backgrounds

**Solution**: Strengthen item negatives
```yaml
items:
  style: "single object, centered, isolated object, no background"
  negative: "multiple objects, scene, background elements, environment, setting, landscape"
```

### Problem: Rooms Have Characters In Them

**Solution**: Add to room negatives
```yaml
rooms:
  negative: "character in scene, people, NPC, person, character sprite, humans, creatures"
```

---

## Advanced Tips

### Tip 1: Layer Your Negatives

```yaml
# Master level - general exclusions
master_style:
  negative_keywords: "3D render, CGI, photorealistic"

# Asset level - specific exclusions
npcs:
  negative: "multiple poses, side view, cropped"

# Enhancement level - quality exclusions
enhancement:
  universal_negatives: ["blurry", "low quality", "distorted"]
```

### Tip 2: Use Prompt Engineering

```yaml
# Instead of just "wizard"
# Use descriptive generation prompts:
"elderly wizard with long white beard and purple robes, friendly expression, full body front view"

# Your style config ensures it's rendered in your game's style!
```

### Tip 3: Test Edge Cases

Generate challenging assets:
```bash
# Complex character
python tools/asset_generator.py npc "robot wizard with mechanical parts" robot_wizard

# Unusual item
python tools/asset_generator.py item "glowing magical crystal" crystal

# Atmospheric room
python tools/asset_generator.py room "foggy mysterious forest clearing" forest
```

If these work well, your style config is solid!

### Tip 4: Document Your Style

```yaml
# Add comments to remember your choices
master_style:
  # Using 2D cartoon to match our existing NPCs
  art_style: "2D cartoon illustration"

  # Heavy negatives needed to avoid 3D renders
  negative_keywords: "3D render, CGI, photorealistic..."

  # Reference: Inspired by Monkey Island and Day of the Tentacle
  additional: "classic LucasArts style"
```

---

## Related Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Installation instructions
- **[README.md](README.md)** - Complete tool documentation
- **[VOICE_CONFIG_GUIDE.md](VOICE_CONFIG_GUIDE.md)** - Audio voice configuration

---

**Master your game's visual identity! 🎨**
