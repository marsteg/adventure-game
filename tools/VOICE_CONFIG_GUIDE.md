# Voice Configuration Guide

Complete guide to customizing character voices for audio generation.

## Table of Contents
- [Overview](#overview)
- [Configuration File](#configuration-file)
- [Provider-Specific Settings](#provider-specific-settings)
- [Character Voice Mapping](#character-voice-mapping)
- [Finding the Right Voice](#finding-the-right-voice)
- [Voice Cloning (XTTS)](#voice-cloning-xtts)
- [Examples](#examples)

---

## Overview

The voice configuration system allows you to assign unique voices to each character in your game. Each character can have different voice settings for each TTS provider (SpeechT5, XTTS, KugelAudio).

**File Location**: `tools/voice_config.yaml`

---

## Configuration File

Create from template:
```bash
cp tools/voice_config.yaml.example tools/voice_config.yaml
```

### Basic Structure

```yaml
characters:
  character_name:
    description: "Brief description of desired voice"
    speecht5:
      speaker_id: 7306
    xtts:
      speaker_wav: null
      description: "text description"
    kugelaudio:
      voice: "default"
```

---

## Provider-Specific Settings

### SpeechT5 (Microsoft)

**Uses**: Speaker ID from CMU Arctic dataset (0-7325)

```yaml
character_name:
  speecht5:
    speaker_id: 7306  # Pick from 0-7325
```

**Common Voice IDs**:
| ID | Voice Type | Best For |
|----|------------|----------|
| 7306 | Neutral female | Professional, mature women |
| 1088 | Younger female | Young characters, ethereal voices |
| 3575 | Medium male | Versatile, most male characters |
| 5142 | Older/deeper male | Authority figures, elderly characters |

**Finding More Voices**:
- Experiment with different IDs (0-7325)
- Test a few and pick the best match
- No need to listen to all 7,326 voices!

### XTTS-v2 (Coqui TTS)

**Features**: Voice cloning from audio samples

```yaml
character_name:
  xtts:
    speaker_wav: "path/to/voice_sample.wav"  # Optional
    description: "text description of voice"
```

**Without Voice Sample** (uses default):
```yaml
zeus:
  xtts:
    speaker_wav: null
    description: "powerful male, deep voice, god-like authority"
```

**With Voice Cloning**:
```yaml
zeus:
  xtts:
    speaker_wav: "assets/voice_samples/zeus_reference.wav"
    description: "powerful male voice"  # Backup description
```

### KugelAudio

**Uses**: Voice presets

```yaml
character_name:
  kugelaudio:
    voice: "default"  # Options: "default", "warm", "clear"
```

---

## Character Voice Mapping

### Pre-Configured Characters

The system comes with 18 pre-configured characters. Here's the current mapping:

**Female Characters**:
```yaml
librarian:
  description: "Mature female librarian, mysterious, slightly sarcastic"
  speecht5:
    speaker_id: 7306  # Neutral female

oracle:
  description: "Mystical female oracle, ethereal and wise"
  speecht5:
    speaker_id: 1088  # Younger, ethereal female

vampire_victoria:
  description: "Teenage female vampire, eternally 17"
  speecht5:
    speaker_id: 1088  # Young female
```

**Male Characters - Authority Figures**:
```yaml
zeus:
  description: "Powerful male god, booming voice"
  speecht5:
    speaker_id: 5142  # Deep, authoritative

dean_malvora:
  description: "Authoritative male dean, formal and imposing"
  speecht5:
    speaker_id: 5142  # Deep, formal

sir_portrait:
  description: "Elderly aristocratic male, formal and dramatic"
  speecht5:
    speaker_id: 5142  # Older male
```

**Male Characters - Casual/Medium**:
```yaml
wolfboy:
  description: "Young male werewolf student, casual"
  speecht5:
    speaker_id: 3575  # Medium male

chef_gronk:
  description: "Gruff male chef, working-class"
  speecht5:
    speaker_id: 3575  # Medium male, gruff

shopkeeper:
  description: "Nervous male shopkeeper"
  speecht5:
    speaker_id: 3575  # Medium male
```

**Special Characters**:
```yaml
planty:
  description: "Sentient plant, wise and condescending, gender-neutral"
  speecht5:
    speaker_id: 7306  # Neutral voice

ghost_timmy:
  description: "Young boy ghost, playful and innocent"
  speecht5:
    speaker_id: 1088  # Young voice

tick_tock:
  description: "Mechanical golem, loud robotic voice"
  speecht5:
    speaker_id: 3575  # Medium male (robotic enough)
```

---

## Finding the Right Voice

### Method 1: Use Pre-Configured Voices

Start with the defaults and adjust if needed:
1. Generate audio for a character
2. Listen to the result
3. If it doesn't match, try a different speaker_id

### Method 2: Test Different Speaker IDs

```bash
# Generate test audio with different voices
python tools/asset_generator.py --generate-audio librarian  # Uses 7306
```

Then edit `voice_config.yaml` and try:
```yaml
librarian:
  speecht5:
    speaker_id: 1088  # Try younger voice
```

Generate again and compare.

### Method 3: Voice ID Ranges

**General guidelines**:
- **0-2000**: Mix of various voices
- **2000-4000**: More male voices
- **4000-6000**: More female voices
- **6000-7325**: Mix, including notable ones like 7306

**Experiment**:
```yaml
your_character:
  speecht5:
    speaker_id: 2543  # Try random IDs
```

### Method 4: Character Archetypes

**For Authority Figures**:
```yaml
  speaker_id: 5142  # Deep, commanding
```

**For Young Characters**:
```yaml
  speaker_id: 1088  # Youthful, light
```

**For Neutral/Professional**:
```yaml
  speaker_id: 7306  # Clear, neutral
```

**For Versatile Male**:
```yaml
  speaker_id: 3575  # Works for most males
```

---

## Voice Cloning (XTTS)

### Requirements

1. **High-quality audio sample** (6-30 seconds)
   - Clear speech, no background noise
   - Single speaker
   - Natural delivery
   - WAV format recommended

2. **Reference text** matches sample content (optional but helpful)

### Steps

#### 1. Prepare Voice Sample

Record or find a clean audio clip:
```
assets/voice_samples/zeus_voice.wav
```

**Quality checklist**:
- ✅ 6-30 seconds long
- ✅ Clear audio, no noise
- ✅ Natural speaking pace
- ✅ Single speaker
- ✅ Represents desired voice style

#### 2. Configure Character

```yaml
zeus:
  xtts:
    speaker_wav: "assets/voice_samples/zeus_voice.wav"
    description: "powerful male voice, deep and commanding"
```

#### 3. Switch to XTTS Provider

In `tools/config.yaml`:
```yaml
audio_provider: "xtts"
```

#### 4. Generate Audio

```bash
python tools/asset_generator.py --generate-audio zeus
```

The system will clone the voice from your sample!

### Tips for Voice Cloning

**✅ Do**:
- Use professional voice acting if possible
- Record in quiet environment
- Keep consistent volume
- Use clear, expressive delivery

**❌ Avoid**:
- Background music or noise
- Multiple speakers in sample
- Phone call quality
- Overly processed audio
- Very short samples (<6 sec)

---

## Examples

### Example 1: Simple Setup (SpeechT5)

```yaml
characters:
  hero:
    description: "Young adventurer, male, confident"
    speecht5:
      speaker_id: 3575
    xtts:
      speaker_wav: null
      description: "young male, confident adventurer"
    kugelaudio:
      voice: "default"

  villain:
    description: "Evil overlord, deep menacing voice"
    speecht5:
      speaker_id: 5142
    xtts:
      speaker_wav: null
      description: "deep male voice, menacing and evil"
    kugelaudio:
      voice: "default"
```

### Example 2: With Voice Cloning

```yaml
characters:
  narrator:
    description: "Professional narrator voice"
    speecht5:
      speaker_id: 7306
    xtts:
      speaker_wav: "assets/voice_samples/narrator.wav"
      description: "clear professional narrator"
    kugelaudio:
      voice: "clear"

  main_character:
    description: "Protagonist with unique voice"
    speecht5:
      speaker_id: 3575
    xtts:
      speaker_wav: "assets/voice_samples/protagonist.wav"
      description: "young hero voice"
    kugelaudio:
      voice: "default"
```

### Example 3: Multiple Characters, Same Voice Type

```yaml
characters:
  guard_1:
    description: "Guard #1"
    speecht5:
      speaker_id: 3575

  guard_2:
    description: "Guard #2"
    speecht5:
      speaker_id: 3576  # Slightly different ID

  guard_3:
    description: "Guard #3"
    speecht5:
      speaker_id: 3577  # Another close ID
```

*Tip: Use adjacent IDs (3575, 3576, 3577) for similar but distinct voices*

---

## Testing Your Voices

### 1. Generate Test Audio

```bash
# Single character
python tools/asset_generator.py --generate-audio librarian
```

### 2. Listen and Compare

```bash
# Check generated files
ls -lh assets/sounds/dialogs/librarian-*.wav

# Play a file (macOS)
afplay assets/sounds/dialogs/librarian-start.wav

# Play a file (Linux)
aplay assets/sounds/dialogs/librarian-start.wav
```

### 3. Adjust if Needed

Edit `voice_config.yaml`:
```yaml
librarian:
  speecht5:
    speaker_id: 1088  # Try different voice
```

Regenerate:
```bash
python tools/asset_generator.py --generate-audio librarian
```

### 4. Compare Results

Listen to both versions and pick the best!

---

## Default Fallback

If a character isn't in `voice_config.yaml`, the system uses the default:

```yaml
characters:
  default:
    description: "Generic neutral voice"
    speecht5:
      speaker_id: 7306
    xtts:
      speaker_wav: null
      description: "neutral voice"
    kugelaudio:
      voice: "default"
```

**This means**: Every character will get a voice even if not configured!

---

## Advanced: Voice Consistency

### For a Cohesive Cast

**Limit voice variety**:
- Use 3-4 speaker IDs total
- Assign based on character archetype
- Keep similar characters consistent

**Example**:
```yaml
# All authority figures use 5142
zeus:        { speecht5: { speaker_id: 5142 }}
dean:        { speecht5: { speaker_id: 5142 }}
professor:   { speecht5: { speaker_id: 5142 }}

# All students use 3575
student_1:   { speecht5: { speaker_id: 3575 }}
student_2:   { speecht5: { speaker_id: 3575 }}
student_3:   { speecht5: { speaker_id: 3575 }}
```

### For Maximum Variety

**Use many different IDs**:
```yaml
char_1:  { speecht5: { speaker_id: 1088 }}
char_2:  { speecht5: { speaker_id: 2543 }}
char_3:  { speecht5: { speaker_id: 4201 }}
char_4:  { speecht5: { speaker_id: 5932 }}
char_5:  { speecht5: { speaker_id: 7306 }}
```

---

## Related Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Installation instructions
- **[README.md](README.md)** - Complete tool documentation
- **[STYLE_CONFIG_GUIDE.md](STYLE_CONFIG_GUIDE.md)** - Image style configuration

---

**Make every character sound unique! 🎭🔊**
