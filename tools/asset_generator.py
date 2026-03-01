#!/usr/bin/env python3
"""
Asset Generator for Point & Click Adventure Game Engine
Generates game assets (NPCs, Rooms, Items, Doors) and audio using AI.
"""

import os
import sys
import argparse
import yaml
import json
import requests
import random
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import base64
import warnings

# Suppress known harmless warnings from TTS and transformers libraries
warnings.filterwarnings('ignore', category=FutureWarning, module='transformers')
warnings.filterwarnings('ignore', category=FutureWarning, module='TTS')
warnings.filterwarnings('ignore', message='.*torch.load.*weights_only.*')

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")

# Import Hugging Face SDK
try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except ImportError:
    print("Warning: huggingface_hub not installed. Install with: pip install huggingface_hub")
    HF_AVAILABLE = False

try:
    from PIL import Image
    import io
except ImportError:
    print("Warning: PIL not available. Install with: pip install Pillow")
    Image = None
    io = None

# Check NumPy version before attempting rembg import to prevent segfault
try:
    import numpy as np
    numpy_version = tuple(map(int, np.__version__.split('.')[:2]))
    if numpy_version[0] >= 2:
        print("=" * 70)
        print("ERROR: NumPy 2.x detected - incompatible with rembg/onnxruntime")
        print("=" * 70)
        print()
        print("Background removal requires NumPy 1.x to avoid crashes.")
        print()
        print("To fix this, run:")
        print("  pip install 'numpy<2'")
        print("  pip install rembg")
        print()
        print("Then restart this tool.")
        print("=" * 70)
        sys.exit(1)
except ImportError:
    print("Warning: NumPy not installed. Installing dependencies...")
    print("Run: pip install -r tools/requirements.txt")
    sys.exit(1)

# Now safe to import rembg
try:
    from PIL import Image
    import io
except ImportError:
    print("Warning: PIL not available. Install with: pip install Pillow")
    Image = None
    io = None

try:
    from rembg import remove
    REMBG_AVAILABLE = True
    print("✓ Background removal enabled")
except ImportError:
    print("Warning: rembg not available. Background removal disabled.")
    print("Install with: pip install rembg")
    REMBG_AVAILABLE = False


class AssetGenerator:
    """Main asset generator class."""

    ASSET_TYPES = {
        'npc': 'assets/npcs',
        'room': 'assets/rooms',
        'item': 'assets/items',
        'door': 'assets/doors'
    }

    # Interactive mode menu items (shown after asset types)
    MENU_ITEMS = [
        'DOUBLE-ASSET',
        'AUDIO-FILES',
        'Exit'
    ]

    def __init__(self, config_path: str = "tools/config.yaml", style_config_path: str = "tools/style_config.yaml"):
        """Initialize the asset generator."""
        self.config_path = Path(config_path)
        self.style_config_path = Path(style_config_path)
        self.voice_config_path = Path("tools/voice_config.yaml")
        self.config = self._load_config()
        self.style_config = self._load_style_config()
        self.voice_config = self._load_voice_config()
        self.usage_file = Path("tools/.usage_tracker.json")
        self.usage = self._load_usage()

        # Initialize Hugging Face client if available
        self.hf_client = None
        if HF_AVAILABLE:
            hf_token = os.getenv('HF_TOKEN')
            if hf_token and hf_token != 'your-huggingface-token-here':
                try:
                    # Initialize with token only - SDK will use correct endpoint
                    self.hf_client = InferenceClient(token=hf_token)
                except Exception as e:
                    print(f"Warning: Failed to initialize Hugging Face client: {e}")

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            print(f"Config file not found at {self.config_path}")
            print("Please copy config.yaml.example to config.yaml and configure it.")
            sys.exit(1)

        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Override with environment variables if present
        if os.getenv('HF_TOKEN'):
            config['huggingface_api_key'] = os.getenv('HF_TOKEN')
        if os.getenv('STABILITY_API_KEY'):
            config['stability_api_key'] = os.getenv('STABILITY_API_KEY')

        return config

    def _load_style_config(self) -> Dict:
        """Load style configuration from YAML file."""
        if not self.style_config_path.exists():
            print(f"Warning: Style config not found at {self.style_config_path}")
            print("Using default styles. Create style_config.yaml for custom styles.")
            return {"master_style": {}, "enhancement": {}}

        with open(self.style_config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_voice_config(self) -> Dict:
        """Load voice configuration for characters."""
        if not self.voice_config_path.exists():
            print(f"Warning: Voice config not found at {self.voice_config_path}")
            print("Using default voices. Create voice_config.yaml to customize character voices.")
            return {"characters": {"default": {}}}

        with open(self.voice_config_path, 'r') as f:
            return yaml.safe_load(f)

    def _get_voice_settings(self, character_name: str, provider: str) -> Dict:
        """Get voice settings for a specific character and provider.

        Args:
            character_name: Character name (e.g., 'librarian', 'zeus')
            provider: TTS provider name (e.g., 'speecht5', 'xtts', 'kugelaudio')

        Returns:
            Dict with provider-specific voice settings
        """
        characters = self.voice_config.get('characters', {})

        # Try to find character-specific settings
        char_config = characters.get(character_name, characters.get('default', {}))

        # Get provider-specific settings
        provider_settings = char_config.get(provider, {})

        # Fall back to default if character not found
        if not provider_settings and character_name != 'default':
            default_config = characters.get('default', {})
            provider_settings = default_config.get(provider, {})

        return provider_settings

    def _load_usage(self) -> Dict:
        """Load usage tracker."""
        if self.usage_file.exists():
            with open(self.usage_file, 'r') as f:
                return json.load(f)
        return {"month": datetime.now().strftime("%Y-%m"), "count": 0}

    def _save_usage(self):
        """Save usage tracker."""
        current_month = datetime.now().strftime("%Y-%m")
        if self.usage["month"] != current_month:
            self.usage = {"month": current_month, "count": 0}

        self.usage_file.parent.mkdir(exist_ok=True)
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f)

    def _increment_usage(self):
        """Increment usage counter."""
        self.usage["count"] += 1
        self._save_usage()

    def _should_remove_background(self, asset_type: str) -> bool:
        """Check if background should be removed for this asset type.

        Args:
            asset_type: Type of asset (npc, room, item, door)

        Returns:
            bool: True if background should be removed
        """
        # Get from config, with default fallback
        bg_config = self.config.get('remove_background', {})
        # NPCs and items default to True, rooms and doors default to False
        default = asset_type in ['npc', 'item']
        return bg_config.get(asset_type, default)

    def check_usage_limit(self) -> bool:
        """Check if usage limit is reached."""
        current_month = datetime.now().strftime("%Y-%m")
        if self.usage["month"] != current_month:
            self.usage = {"month": current_month, "count": 0}

        limit = self.config.get('monthly_limit', 25)
        remaining = limit - self.usage["count"]

        provider = self.config.get('provider', 'huggingface').lower()

        # For Hugging Face, show usage tracking but no real limit
        if provider in ['huggingface', 'hf']:
            print(f"Images generated this month: {self.usage['count']} (Hugging Face - unlimited)")
            return True

        # For Stability AI, show actual limits
        print(f"Monthly usage: {self.usage['count']}/{limit} (Remaining: {remaining})")

        if self.usage["count"] >= limit:
            print("⚠️  Monthly limit reached!")
            print("💡 Switch to Hugging Face for unlimited free generation:")
            print("   Set provider: 'huggingface' in config.yaml")
            return False
        return True

    def build_prompt(self, asset_type: str, description: str) -> tuple[str, str]:
        """Build a complete prompt for the asset type with negative prompt.

        Returns:
            tuple: (positive_prompt, negative_prompt)
        """
        # Get master style configuration
        master_style = self.style_config.get('master_style', {})
        art_style = master_style.get('art_style', '')
        detail_level = master_style.get('detail_level', '')
        color_style = master_style.get('color_style', '')
        master_additional = master_style.get('additional', '')

        # Get asset-specific style overrides
        asset_config = self.style_config.get(asset_type + 's', {})  # 'npcs', 'rooms', etc.
        asset_style = asset_config.get('style', '')
        asset_additional = asset_config.get('additional', '')

        # Get quality boosters
        enhancement = self.style_config.get('enhancement', {})
        quality_boosters = enhancement.get('quality_boosters', [])
        quality_str = ', '.join(quality_boosters) if quality_boosters else ''

        # Build positive prompt
        prompt_parts = [description]

        # Add asset-specific style
        if asset_style:
            prompt_parts.append(asset_style)

        # Add master style
        if art_style:
            prompt_parts.append(art_style)
        if detail_level:
            prompt_parts.append(detail_level)
        if color_style:
            prompt_parts.append(color_style)

        # Add quality boosters
        if quality_str:
            prompt_parts.append(quality_str)

        # Add additional notes
        if asset_additional:
            prompt_parts.append(asset_additional)
        if master_additional:
            prompt_parts.append(master_additional)

        # Background handling - add transparent background hint for assets that will have bg removed
        if self._should_remove_background(asset_type):
            prompt_parts.append("transparent background, isolated on white")

        positive_prompt = ', '.join(prompt_parts)

        # Build negative prompt
        negative_parts = []

        # Master negative keywords (most important!)
        master_negatives = master_style.get('negative_keywords', '')
        if master_negatives:
            negative_parts.append(master_negatives)

        # Asset-specific negatives
        asset_negatives = asset_config.get('negative', '')
        if asset_negatives:
            negative_parts.append(asset_negatives)

        # Universal negatives from enhancement config
        universal_negatives = enhancement.get('universal_negatives', [])
        if universal_negatives:
            negative_parts.extend(universal_negatives)

        negative_prompt = ', '.join(negative_parts)

        return positive_prompt.strip(), negative_prompt.strip()

    def generate_image_huggingface(self, prompt: str, negative_prompt: str, asset_type: str,
                                   width: int = None, height: int = None, seed: int = None) -> Optional[bytes]:
        """Generate image using Hugging Face Inference API (FREE!).

        Args:
            prompt: Positive prompt
            negative_prompt: Negative prompt
            asset_type: Type of asset (for default dimensions)
            width: Override width (None = use config)
            height: Override height (None = use config)
            seed: Random seed for reproducible generation (None = random)
        """
        if not HF_AVAILABLE:
            print("Error: huggingface_hub not installed.")
            print("Install with: pip install huggingface_hub")
            return None

        if not self.hf_client:
            hf_token = os.getenv('HF_TOKEN')
            if not hf_token or hf_token == 'your-huggingface-token-here':
                print("Error: Please set HF_TOKEN in .env file")
                print("Get a FREE token at: https://huggingface.co/settings/tokens")
                print("Then add it to .env file: HF_TOKEN=hf_your_token")
                return None

            try:
                self.hf_client = InferenceClient(token=hf_token)
            except Exception as e:
                print(f"Error initializing Hugging Face client: {e}")
                return None

        model = self.config.get('huggingface_model', 'black-forest-labs/FLUX.1-schnell')

        print(f"Generating with style: {self.style_config.get('master_style', {}).get('art_style', 'default')}")
        print(f"Provider: Hugging Face (FREE, unlimited)")
        print(f"Model: {model.split('/')[-1]}")

        # FLUX models work better with negative prompts integrated into the main prompt
        if 'flux' in model.lower():
            # Build comprehensive prompt with style and negative keywords
            art_style = self.style_config.get('master_style', {}).get('art_style', '')
            full_prompt = f"{prompt}"
            if art_style:
                full_prompt += f". Style: {art_style}"
            if negative_prompt:
                # Take first 100 chars of negative prompt to keep it concise
                full_prompt += f". Avoid: {negative_prompt[:100]}"

            print(f"Prompt: {full_prompt[:150]}...")
        else:
            full_prompt = prompt
            print(f"Prompt: {prompt[:100]}..." if len(prompt) > 100 else f"Prompt: {prompt}")
            print(f"Negative: {negative_prompt[:80]}..." if len(negative_prompt) > 80 else f"Negative: {negative_prompt}")

        print("Please wait (may take 20-60 seconds for free tier)...")

        try:
            # Get dimensions: use override if provided, otherwise config default
            if width is None or height is None:
                dimensions = self.config.get('dimensions', {}).get(asset_type, [1024, 1024])
                width = width or dimensions[0]
                height = height or dimensions[1]

            print(f"Size: {width}x{height}")

            # Generate seed if not provided
            if seed is None:
                seed = random.randint(0, 999999)
            print(f"Seed: {seed}")

            # Generate image using SDK
            image = self.hf_client.text_to_image(
                prompt=full_prompt,
                model=model,
                width=width,
                height=height,
                seed=seed,
            )

            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()

            print("✓ Image generated successfully!")
            self._increment_usage()
            return img_bytes

        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    def generate_image_stability(self, prompt: str, negative_prompt: str, asset_type: str,
                                width: int = None, height: int = None, seed: int = None) -> Optional[bytes]:
        """Generate image using Stability AI API (LIMITED FREE TIER).

        Args:
            prompt: Positive prompt
            negative_prompt: Negative prompt
            asset_type: Type of asset (for default dimensions)
            width: Override width (None = use config)
            height: Override height (None = use config)
            seed: Random seed for reproducible generation (None = random)
        """
        api_key = os.getenv('STABILITY_API_KEY') or self.config.get('stability_api_key')
        if not api_key or api_key == 'your-api-key-here':
            print("Error: Please set STABILITY_API_KEY in .env file")
            print("Get a free API key at: https://platform.stability.ai/")
            print("Note: Free tier only gives ~3 images. Consider using Hugging Face instead!")
            return None

        # Use Stable Diffusion 3.5 Large (free tier compatible)
        url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

        headers = {
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        }

        # Get dimensions: use override if provided, otherwise config default
        if width is None or height is None:
            dimensions = self.config.get('dimensions', {}).get(asset_type, [1024, 1024])
            width = width or dimensions[0]
            height = height or dimensions[1]

        # Calculate aspect ratio for Stability AI (they use aspect_ratio, not exact dimensions)
        if width == height:
            aspect_ratio = "1:1"
        elif width > height:
            aspect_ratio = "16:9" if width / height > 1.5 else "4:3"
        else:
            aspect_ratio = "9:16" if height / width > 1.5 else "3:4"

        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "mode": "text-to-image"
        }

        # Add seed if provided
        if seed is not None:
            data["seed"] = seed

        print(f"Generating with style: {self.style_config.get('master_style', {}).get('art_style', 'default')}")
        print(f"Provider: Stability AI (Limited free tier)")
        print(f"Size: ~{width}x{height} (aspect ratio: {aspect_ratio})")
        if seed is not None:
            print(f"Seed: {seed}")
        print(f"Prompt: {prompt[:100]}..." if len(prompt) > 100 else f"Prompt: {prompt}")
        print(f"Negative: {negative_prompt[:80]}..." if len(negative_prompt) > 80 else f"Negative: {negative_prompt}")
        print("Please wait...")

        try:
            response = requests.post(url, headers=headers, files={"none": ''}, data=data)

            if response.status_code == 200:
                print("✓ Image generated successfully!")
                self._increment_usage()
                return response.content
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                return None

        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    def generate_image(self, prompt: str, negative_prompt: str, asset_type: str,
                      width: int = None, height: int = None, seed: int = None) -> Optional[bytes]:
        """Generate image using configured provider.

        Args:
            prompt: Positive prompt
            negative_prompt: Negative prompt
            asset_type: Type of asset (for default dimensions)
            width: Override width (None = use config)
            height: Override height (None = use config)
            seed: Random seed for reproducible generation (None = random)
        """
        provider = self.config.get('provider', 'huggingface').lower()

        if provider == 'huggingface' or provider == 'hf':
            return self.generate_image_huggingface(prompt, negative_prompt, asset_type, width, height, seed)
        elif provider == 'stability' or provider == 'stabilityai':
            return self.generate_image_stability(prompt, negative_prompt, asset_type, width, height, seed)
        else:
            print(f"Unknown provider: {provider}")
            print("Valid providers: 'huggingface' (default, free) or 'stability'")
            return None

    def remove_background(self, image_data: bytes) -> Optional[bytes]:
        """Remove background from image."""
        if not REMBG_AVAILABLE:
            print("Background removal not available. Install rembg library.")
            return image_data

        if not Image or not io:
            print("PIL not available. Skipping background removal.")
            return image_data

        try:
            print("Removing background...")
            input_image = Image.open(io.BytesIO(image_data))
            output_image = remove(input_image)

            # Convert to bytes
            output_buffer = io.BytesIO()
            output_image.save(output_buffer, format='PNG')
            print("✓ Background removed!")
            return output_buffer.getvalue()
        except Exception as e:
            print(f"Error removing background: {e}")
            return image_data

    def generate_audio(self, text: str, character_name: str = None, filename_hint: str = "") -> Optional[bytes]:
        """Generate audio using configured provider.

        Args:
            text: Text to convert to speech
            character_name: Character name for voice customization (e.g., 'librarian')
            filename_hint: Hint for usage tracking (e.g., "librarian-start")

        Returns:
            bytes: WAV audio data or None if failed
        """
        provider = self.config.get('audio_provider', 'speecht5').lower()

        if provider == 'speecht5':
            return self.generate_audio_speecht5(text, character_name, filename_hint)
        elif provider == 'xtts':
            return self.generate_audio_xtts(text, character_name, filename_hint)
        elif provider == 'kugelaudio':
            return self.generate_audio_kugelaudio(text, character_name, filename_hint)
        else:
            print(f"Unknown audio provider: {provider}")
            print("Valid providers: 'speecht5', 'xtts', 'kugelaudio'")
            return None

    def _get_default_xtts_speaker(self) -> Optional[str]:
        """Get or download a default speaker sample for XTTS.

        Returns path to a cached default speaker WAV file.
        """
        # Cache path for default speaker
        cache_dir = Path.home() / ".cache" / "asset_generator"
        cache_dir.mkdir(parents=True, exist_ok=True)
        default_speaker_path = cache_dir / "xtts_default_speaker.wav"

        # If already cached, return it
        if default_speaker_path.exists():
            return str(default_speaker_path)

        # Download a sample speaker from XTTS examples
        try:
            import requests
            print("Downloading default XTTS speaker sample (one-time)...")
            # Use a female voice sample from the XTTS-v2 examples on HuggingFace
            url = "https://huggingface.co/coqui/XTTS-v2/resolve/main/samples/en_sample.wav"
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Save to cache
            with open(default_speaker_path, 'wb') as f:
                f.write(response.content)

            print(f"✓ Default speaker cached to: {default_speaker_path}")
            return str(default_speaker_path)

        except Exception as e:
            print(f"Error downloading default speaker: {e}")
            return None

    def generate_audio_speecht5(self, text: str, character_name: str = None, filename_hint: str = "") -> Optional[bytes]:
        """Generate audio using Microsoft SpeechT5 model.

        Args:
            text: Text to convert to speech
            character_name: Character name for voice selection
            filename_hint: Hint for logs

        Returns:
            bytes: WAV audio data or None if failed
        """
        # Lazy import to avoid loading on startup
        try:
            import torch
            from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
            from datasets import load_dataset
            import soundfile as sf
        except ImportError as e:
            print("Error: SpeechT5 dependencies not installed.")
            print("Install with: pip install transformers datasets soundfile")
            return None

        print(f"Generating audio with SpeechT5...")
        if character_name:
            print(f"Character: {character_name}")
        print(f"Text: {text[:80]}..." if len(text) > 80 else f"Text: {text}")

        try:
            # Get settings from config
            audio_settings = self.config.get('audio_settings', {}).get('speecht5', {})
            model_name = audio_settings.get('model', 'microsoft/speecht5_tts')
            vocoder_name = audio_settings.get('vocoder', 'microsoft/speecht5_hifigan')
            sample_rate = audio_settings.get('sample_rate', 16000)

            # Get character-specific voice settings
            voice_settings = self._get_voice_settings(character_name or 'default', 'speecht5')
            speaker_id = voice_settings.get('speaker_id', 7306)  # Default to neutral female

            # Get HF token
            hf_token = self.config.get('huggingface_api_key')
            if not hf_token or hf_token == 'your-huggingface-token-here':
                hf_token = os.getenv('HF_TOKEN')

            # Prepare kwargs for model loading
            model_kwargs = {}
            if hf_token and hf_token != 'your-huggingface-token-here':
                model_kwargs['token'] = hf_token

            # Initialize model (cache in instance to avoid reloading)
            if not hasattr(self, '_speecht5_processor'):
                print("Loading SpeechT5 model (first time, may take a minute)...")
                device = "cuda" if torch.cuda.is_available() else "cpu"

                try:
                    # Load tokenizer explicitly first (workaround for transformers bug)
                    from transformers import SpeechT5Tokenizer
                    print("  Loading tokenizer...")
                    tokenizer = SpeechT5Tokenizer.from_pretrained(
                        model_name,
                        trust_remote_code=True,
                        **model_kwargs
                    )

                    # Now load processor with tokenizer
                    print("  Loading processor...")
                    self._speecht5_processor = SpeechT5Processor.from_pretrained(
                        model_name,
                        tokenizer=tokenizer,
                        trust_remote_code=True,
                        **model_kwargs
                    )

                    print("  Loading model...")
                    self._speecht5_model = SpeechT5ForTextToSpeech.from_pretrained(
                        model_name,
                        trust_remote_code=True,
                        **model_kwargs
                    ).to(device)

                    print("  Loading vocoder...")
                    self._speecht5_vocoder = SpeechT5HifiGan.from_pretrained(
                        vocoder_name,
                        trust_remote_code=True,
                        **model_kwargs
                    ).to(device)

                    # Load speaker embeddings dataset
                    print("  Loading speaker embeddings...")
                    # Enable trust_remote_code for datasets library (required for newer versions)
                    os.environ['HF_DATASETS_TRUST_REMOTE_CODE'] = '1'
                    self._speecht5_embeddings_dataset = load_dataset(
                        "Matthijs/cmu-arctic-xvectors",
                        split="validation",
                        **model_kwargs
                    )

                    self._speecht5_device = device
                    print("✓ Model loaded successfully")

                except Exception as e:
                    print(f"Error during model initialization: {e}")
                    import traceback
                    traceback.print_exc()
                    # Clean up partial state
                    if hasattr(self, '_speecht5_processor'):
                        delattr(self, '_speecht5_processor')
                    if hasattr(self, '_speecht5_model'):
                        delattr(self, '_speecht5_model')
                    if hasattr(self, '_speecht5_vocoder'):
                        delattr(self, '_speecht5_vocoder')
                    if hasattr(self, '_speecht5_embeddings_dataset'):
                        delattr(self, '_speecht5_embeddings_dataset')
                    return None

            # Verify all components loaded
            if not hasattr(self, '_speecht5_embeddings_dataset'):
                print("Error: Model components not fully loaded. Try again.")
                return None

            # Get speaker embeddings for this character
            speaker_embeddings = torch.tensor(
                self._speecht5_embeddings_dataset[speaker_id]["xvector"]
            ).unsqueeze(0).to(self._speecht5_device)

            # Prepare input
            inputs = self._speecht5_processor(text=text, return_tensors="pt")
            inputs = {k: v.to(self._speecht5_device) for k, v in inputs.items()}

            # Generate speech
            with torch.no_grad():
                speech = self._speecht5_model.generate_speech(
                    inputs["input_ids"],
                    speaker_embeddings,
                    vocoder=self._speecht5_vocoder
                )

            # Convert to bytes
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_path = tmp_file.name

            # Save as WAV
            sf.write(tmp_path, speech.cpu().numpy(), samplerate=sample_rate)

            # Read bytes
            with open(tmp_path, 'rb') as f:
                audio_bytes = f.read()

            # Clean up temp file
            os.unlink(tmp_path)

            print("✓ Audio generated successfully!")
            self._increment_usage()
            return audio_bytes

        except Exception as e:
            print(f"Error generating audio: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_audio_xtts(self, text: str, character_name: str = None, filename_hint: str = "") -> Optional[bytes]:
        """Generate audio using Coqui XTTS-v2 model.

        Args:
            text: Text to convert to speech
            character_name: Character name for voice cloning/selection
            filename_hint: Hint for logs

        Returns:
            bytes: WAV audio data or None if failed
        """
        # Lazy import to avoid loading on startup
        try:
            from TTS.api import TTS
        except ImportError:
            print("Error: Coqui TTS not installed.")
            print("Install with: pip install TTS")
            return None

        print(f"Generating audio with XTTS-v2...")
        if character_name:
            print(f"Character: {character_name}")
        print(f"Text: {text[:80]}..." if len(text) > 80 else f"Text: {text}")

        try:
            # Get settings from config
            audio_settings = self.config.get('audio_settings', {}).get('xtts', {})
            model_name = audio_settings.get('model', 'tts_models/multilingual/multi-dataset/xtts_v2')
            language = audio_settings.get('language', 'en')

            # Get character-specific voice settings
            voice_settings = self._get_voice_settings(character_name or 'default', 'xtts')
            speaker_wav = voice_settings.get('speaker_wav')

            # Initialize model (cache in instance to avoid reloading)
            if not hasattr(self, '_xtts_model'):
                print("Loading XTTS-v2 model (first time, may take a minute)...")
                self._xtts_model = TTS(model_name)
                print("✓ Model loaded successfully")

            # Generate speech to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_path = tmp_file.name

            if speaker_wav and os.path.exists(speaker_wav):
                # Voice cloning mode with character-specific reference
                print(f"Using voice cloning with: {speaker_wav}")
                self._xtts_model.tts_to_file(
                    text=text,
                    speaker_wav=speaker_wav,
                    language=language,
                    file_path=tmp_path
                )
            else:
                # XTTS requires a speaker reference for voice cloning
                # Fallback to generic female voice sample from XTTS examples
                print("⚠️  No speaker_wav configured - using default voice")
                print("   Tip: Configure character voices in tools/voice_config.yaml for better results!")

                # Download and cache a default speaker sample
                default_speaker = self._get_default_xtts_speaker()
                if default_speaker and os.path.exists(default_speaker):
                    self._xtts_model.tts_to_file(
                        text=text,
                        speaker_wav=default_speaker,
                        language=language,
                        file_path=tmp_path
                    )
                else:
                    print("Error: Could not load default speaker. Please configure speaker_wav in voice_config.yaml")
                    return None

            # Read bytes
            with open(tmp_path, 'rb') as f:
                audio_bytes = f.read()

            # Clean up temp file
            os.unlink(tmp_path)

            print("✓ Audio generated successfully!")
            self._increment_usage()
            return audio_bytes

        except Exception as e:
            print(f"Error generating audio: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_audio_kugelaudio(self, text: str, character_name: str = None, filename_hint: str = "") -> Optional[bytes]:
        """Generate audio using KugelAudio model from HuggingFace.

        Args:
            text: Text to convert to speech
            character_name: Character name for voice selection
            filename_hint: Hint for logs

        Returns:
            bytes: WAV audio data or None if failed
        """
        # Lazy import to avoid loading on startup
        try:
            import torch
            from kugelaudio_open import (
                KugelAudioForConditionalGenerationInference,
                KugelAudioProcessor,
            )
        except ImportError:
            print("Error: kugelaudio-open not installed.")
            print("Install: git clone https://github.com/Kugelaudio/kugelaudio-open.git")
            print("        cd kugelaudio-open && uv sync")
            return None

        # Check token
        hf_token = self.config.get('huggingface_api_key')
        if not hf_token or hf_token == 'your-huggingface-token-here':
            hf_token = os.getenv('HF_TOKEN')
        if not hf_token or hf_token == 'your-huggingface-token-here':
            print("Error: Please set HF_TOKEN in .env file")
            print("Get a FREE token at: https://huggingface.co/settings/tokens")
            return None

        print(f"Generating audio with KugelAudio...")
        if character_name:
            print(f"Character: {character_name}")
        print(f"Text: {text[:80]}..." if len(text) > 80 else f"Text: {text}")

        try:
            # Get settings from config
            audio_settings = self.config.get('audio_settings', {}).get('kugelaudio', {})
            cfg_scale = audio_settings.get('cfg_scale', 3.0)
            max_new_tokens = audio_settings.get('max_new_tokens', 2048)

            # Get character-specific voice settings
            voice_settings = self._get_voice_settings(character_name or 'default', 'kugelaudio')
            voice = voice_settings.get('voice', 'default')

            # Initialize model (cache in instance to avoid reloading)
            if not hasattr(self, '_kugelaudio_model'):
                print("Loading KugelAudio model (first time, may take a minute)...")
                device = "cuda" if torch.cuda.is_available() else "cpu"

                self._kugelaudio_model = KugelAudioForConditionalGenerationInference.from_pretrained(
                    "kugelaudio/kugelaudio-0-open",
                    torch_dtype=torch.bfloat16,
                    token=hf_token
                ).to(device)
                self._kugelaudio_model.eval()

                # Strip encoder weights to save VRAM
                self._kugelaudio_model.model.strip_encoders()

                self._kugelaudio_processor = KugelAudioProcessor.from_pretrained(
                    "kugelaudio/kugelaudio-0-open",
                    token=hf_token
                )
                self._kugelaudio_device = device
                print("✓ Model loaded successfully")

            # Prepare input
            inputs = self._kugelaudio_processor(
                text=text,
                voice=voice,
                return_tensors="pt"
            )
            inputs = {
                k: v.to(self._kugelaudio_device) if isinstance(v, torch.Tensor) else v
                for k, v in inputs.items()
            }

            # Generate speech
            with torch.no_grad():
                outputs = self._kugelaudio_model.generate(
                    **inputs,
                    cfg_scale=cfg_scale,
                    max_new_tokens=max_new_tokens
                )

            # Save to temporary file and read bytes
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_path = tmp_file.name

            self._kugelaudio_processor.save_audio(outputs.speech_outputs[0], tmp_path)

            # Read bytes
            with open(tmp_path, 'rb') as f:
                audio_bytes = f.read()

            # Clean up temp file
            os.unlink(tmp_path)

            print("✓ Audio generated successfully!")
            self._increment_usage()
            return audio_bytes

        except Exception as e:
            print(f"Error generating audio: {e}")
            import traceback
            traceback.print_exc()
            return None

    def save_audio(self, audio_data: bytes, character_name: str, dialog_id: str) -> Optional[Path]:
        """Save audio file to dialogs directory.

        Args:
            audio_data: WAV audio bytes
            character_name: Character name (e.g., 'librarian')
            dialog_id: Dialog node ID (e.g., 'start', 'description-locked')

        Returns:
            Path to saved file or None
        """
        audio_dir = Path("assets/sounds/dialogs")
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Clean names
        clean_character = character_name.lower().replace(' ', '_').replace('-', '_')
        clean_dialog = dialog_id.lower().replace(' ', '_')

        filename = f"{clean_character}-{clean_dialog}.wav"
        filepath = audio_dir / filename

        # Handle duplicates (add counter)
        counter = 1
        while filepath.exists():
            filename = f"{clean_character}-{clean_dialog}_{counter}.wav"
            filepath = audio_dir / filename
            counter += 1

        try:
            with open(filepath, 'wb') as f:
                f.write(audio_data)

            print(f"✓ Audio saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving audio: {e}")
            return None

    def parse_dialog_yaml(self, yaml_path: Path) -> Dict[str, List[tuple[str, str]]]:
        """Parse dialog YAML and extract all text that needs audio.

        Args:
            yaml_path: Path to dialog YAML file

        Returns:
            Dict mapping dialog_id to list of (text, suggested_filename) tuples
            Example: {
                'description-locked': [('The librarian...', 'librarian-description-locked')],
                'start': [('Ah, Death\'s daughter...', 'librarian-start')]
            }
        """
        with open(yaml_path, 'r') as f:
            dialog_data = yaml.safe_load(f)

        if not dialog_data:
            print(f"Warning: Empty or invalid YAML file: {yaml_path}")
            return {}

        # Extract character name from filename
        character_name = yaml_path.stem  # e.g., 'librarian' from 'librarian.yaml'

        texts_to_generate = {}

        # Process description section
        if 'description' in dialog_data:
            desc = dialog_data['description']

            # Locked description
            if 'locked' in desc and 'line' in desc['locked']:
                line = desc['locked']['line']
                if line and line.strip():
                    dialog_id = 'description-locked'
                    texts_to_generate[dialog_id] = [(line, f"{character_name}-{dialog_id}")]

            # Unlocked description
            if 'unlocked' in desc and 'line' in desc['unlocked']:
                line = desc['unlocked']['line']
                if line and line.strip():
                    dialog_id = 'description-unlocked'
                    texts_to_generate[dialog_id] = [(line, f"{character_name}-{dialog_id}")]

        # Process dialog nodes
        for node_id, node_data in dialog_data.items():
            # Skip description (already processed)
            if node_id == 'description':
                continue

            # Check if this is a dialog node (has 'line' key)
            if isinstance(node_data, dict) and 'line' in node_data:
                line = node_data['line']

                # Handle both single strings and arrays
                if isinstance(line, str):
                    if line and line.strip():
                        texts_to_generate[node_id] = [(line, f"{character_name}-{node_id}")]
                elif isinstance(line, list):
                    # Array of lines - generate separate files
                    valid_lines = [(text, f"{character_name}-{node_id}-{idx}")
                                   for idx, text in enumerate(line)
                                   if text and text.strip()]
                    if valid_lines:
                        texts_to_generate[node_id] = valid_lines

        return texts_to_generate

    def generate_dialog_audio(self, character_name: str, skip_confirmation: bool = False):
        """Generate audio for all dialog lines of a character.

        Args:
            character_name: Name of the character (must match YAML filename)
            skip_confirmation: If True, skip the confirmation prompt (for CLI use)
        """
        # Find dialog YAML file
        yaml_path = Path(f"assets/dialogs/{character_name}.yaml")

        if not yaml_path.exists():
            print(f"Error: Dialog file not found: {yaml_path}")
            print(f"\nAvailable dialogs:")
            dialog_dir = Path("assets/dialogs")
            if dialog_dir.exists():
                for yaml_file in sorted(dialog_dir.glob("*.yaml")):
                    print(f"  - {yaml_file.stem}")
            return

        print(f"\n=== Generating Audio for {character_name} ===\n")

        # Parse YAML
        print("Parsing dialog YAML...")
        texts = self.parse_dialog_yaml(yaml_path)

        if not texts:
            print("No dialog text found to generate audio for.")
            return

        total_lines = sum(len(lines) for lines in texts.values())
        print(f"Found {len(texts)} dialog nodes with {total_lines} total lines\n")

        # Confirm before proceeding (can be expensive)
        if not skip_confirmation:
            confirm = input(f"Generate {total_lines} audio files? This may take several minutes. (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                return
        else:
            print(f"Generating {total_lines} audio files...")

        # Generate audio for each line
        generated_count = 0
        failed_count = 0

        for node_id, lines in texts.items():
            for text, suggested_filename in lines:
                print(f"\n[{generated_count + failed_count + 1}/{total_lines}] Generating: {node_id}")

                # Generate audio with character-specific voice
                audio_data = self.generate_audio(text, character_name, suggested_filename)

                if audio_data:
                    # Save audio
                    filepath = self.save_audio(audio_data, character_name, node_id)
                    if filepath:
                        generated_count += 1
                    else:
                        failed_count += 1
                else:
                    print(f"✗ Failed to generate audio for: {node_id}")
                    failed_count += 1

        # Summary
        print(f"\n=== Generation Complete ===")
        print(f"✓ Successfully generated: {generated_count}/{total_lines}")
        if failed_count > 0:
            print(f"✗ Failed: {failed_count}/{total_lines}")

    def save_asset(self, image_data: bytes, asset_type: str, name: str):
        """Save asset to appropriate directory."""
        asset_dir = Path(self.ASSET_TYPES[asset_type])
        asset_dir.mkdir(parents=True, exist_ok=True)

        # Clean filename
        clean_name = name.lower().replace(' ', '_').replace('-', '_')
        filepath = asset_dir / f"{clean_name}.png"

        # Handle duplicates
        counter = 1
        while filepath.exists():
            filepath = asset_dir / f"{clean_name}_{counter}.png"
            counter += 1

        with open(filepath, 'wb') as f:
            f.write(image_data)

        print(f"✓ Asset saved to: {filepath}")
        return filepath

    def generate_asset(self, asset_type: str, description: str, name: str,
                      remove_bg: bool = None, width: int = None, height: int = None, seed: int = None) -> Optional[Path]:
        """Generate a single asset.

        Args:
            asset_type: Type of asset (npc, room, item, door)
            description: Text description of the asset
            name: Filename for the asset
            remove_bg: Override background removal setting (None = use config)
            width: Override width (None = use config default)
            height: Override height (None = use config default)
            seed: Random seed for reproducible generation (None = random)
        """
        if not self.check_usage_limit():
            return None

        # Build prompt with style configuration
        positive_prompt, negative_prompt = self.build_prompt(asset_type, description)

        # Generate image with optional size override and seed
        image_data = self.generate_image(positive_prompt, negative_prompt, asset_type, width, height, seed)
        if not image_data:
            return None

        # Remove background based on config (unless explicitly overridden)
        if remove_bg is None:
            remove_bg = self._should_remove_background(asset_type)

        if remove_bg:
            image_data = self.remove_background(image_data)

        # Save asset
        filepath = self.save_asset(image_data, asset_type, name)
        return filepath

    def generate_double_asset(self, asset_type: str,
                             base_description: str,
                             variation_description: str,
                             base_name: str,
                             variation_name: str,
                             shared_traits: str = "",
                             remove_bg: bool = None,
                             width: int = None,
                             height: int = None) -> tuple[Optional[Path], Optional[Path]]:
        """Generate two variations of the same asset with improved consistency.

        Args:
            asset_type: Type of asset (npc, room, item, door)
            base_description: Description of the base/original asset
            variation_description: Description of the variation
            base_name: Filename for base asset
            variation_name: Filename for variation asset
            shared_traits: Shared characteristics for consistency (composition, angle, etc.)
            remove_bg: Background removal setting
            width: Image width
            height: Image height

        Returns:
            tuple: (base_filepath, variation_filepath) or (None, None) if failed
        """
        # Generate shared seed for consistency
        seed = random.randint(0, 999999)
        print(f"\nUsing seed {seed} for consistency between variations...")

        # Add shared traits to both descriptions if provided
        if shared_traits:
            base_full = f"{base_description}, {shared_traits}"
            variation_full = f"{variation_description}, {shared_traits}"
        else:
            base_full = base_description
            variation_full = variation_description

        print("\n=== Generating Base Asset ===")
        base_path = self.generate_asset(asset_type, base_full, base_name,
                                        remove_bg, width, height, seed)

        if not base_path:
            print("Failed to generate base asset. Aborting.")
            return None, None

        # Add consistency keywords to variation
        consistency_boost = "maintaining same composition, perspective, and art style"
        variation_enhanced = f"{variation_full}, {consistency_boost}"

        print("\n=== Generating Variation ===")
        variation_path = self.generate_asset(asset_type, variation_enhanced,
                                            variation_name, remove_bg, width, height, seed)

        if not variation_path:
            print("Warning: Base asset generated but variation failed.")
            return base_path, None

        print("\n✓ Double-asset generation complete!")
        print(f"  Base: {base_path}")
        print(f"  Variation: {variation_path}")

        return base_path, variation_path

    def list_templates(self, asset_type: Optional[str] = None):
        """List common examples for generating assets."""

        examples = {
            'npc': [
                ('wizard', 'Magical character with staff and robes'),
                ('guard', 'Armored guard with sword or spear'),
                ('shopkeeper', 'Friendly merchant with apron'),
                ('villager', 'Common townsperson'),
                ('monster', 'Fantasy creature or beast'),
                ('knight', 'Armored warrior'),
                ('thief', 'Rogue character in dark clothes'),
                ('priest', 'Religious figure in robes'),
            ],
            'room': [
                ('library', 'Library with bookshelves and reading area'),
                ('tavern', 'Inn or tavern with tables and bar'),
                ('dungeon', 'Dark prison or dungeon cell'),
                ('throne_room', 'Grand royal throne room'),
                ('bedroom', 'Cozy bedroom interior'),
                ('kitchen', 'Cooking area with stove and utensils'),
                ('forest', 'Outdoor forest clearing'),
                ('cave', 'Dark cave interior'),
            ],
            'item': [
                ('key', 'Key for unlocking doors'),
                ('potion', 'Magical potion bottle'),
                ('sword', 'Weapon - sword or blade'),
                ('book', 'Old book or tome'),
                ('gem', 'Precious gemstone or crystal'),
                ('amulet', 'Magical amulet or pendant'),
                ('scroll', 'Ancient scroll or parchment'),
                ('coin', 'Gold coin or currency'),
            ],
            'door': [
                ('wooden_door', 'Simple wooden door'),
                ('metal_door', 'Heavy metal or iron door'),
                ('castle_door', 'Large ornate castle door'),
                ('dungeon_door', 'Prison cell door with bars'),
                ('magic_door', 'Mystical door with runes'),
            ]
        }

        if asset_type:
            if asset_type in examples:
                print(f"\n{asset_type.upper()} Examples:")
                print(f"Use these as inspiration for your descriptions:\n")
                for name, description in examples[asset_type]:
                    print(f"  {name:20} - {description}")
                print(f"\nExample usage:")
                print(f"  python tools/asset_generator.py {asset_type} \"{examples[asset_type][0][0]} character\" {examples[asset_type][0][0]}")
        else:
            for atype in self.ASSET_TYPES.keys():
                self.list_templates(atype)

    def interactive_mode(self):
        """Interactive mode for generating assets."""
        print("\n=== Asset Generator - Interactive Mode ===\n")

        while True:
            # Display asset types
            print("\nAsset Types:")
            for i, atype in enumerate(self.ASSET_TYPES.keys(), 1):
                print(f"  {i}. {atype.upper()}")

            # Display additional menu items
            base_num = len(self.ASSET_TYPES)
            for i, menu_item in enumerate(self.MENU_ITEMS, base_num + 1):
                print(f"  {i}. {menu_item}")

            total_options = base_num + len(self.MENU_ITEMS)
            choice = input(f"\nSelect asset type (1-{total_options}): ").strip()

            # Exit check
            exit_num = base_num + len(self.MENU_ITEMS)
            if choice == str(exit_num):
                print("Goodbye!")
                break

            # Audio generation mode
            audio_num = base_num + 2  # Position of AUDIO-FILES in menu
            if choice == str(audio_num):
                print("\n--- Audio Generation Mode ---\n")

                # List available characters
                dialog_dir = Path("assets/dialogs")
                if dialog_dir.exists():
                    yaml_files = sorted(dialog_dir.glob("*.yaml"))
                    print("Available characters:")
                    for i, yaml_file in enumerate(yaml_files, 1):
                        print(f"  {i}. {yaml_file.stem}")
                    print()

                character_name = input("Enter character name (or number from list): ").strip()

                # Handle numeric selection
                if character_name.isdigit() and dialog_dir.exists():
                    yaml_files = sorted(dialog_dir.glob("*.yaml"))
                    idx = int(character_name) - 1
                    if 0 <= idx < len(yaml_files):
                        character_name = yaml_files[idx].stem
                    else:
                        print("Invalid selection!")
                        continue

                if character_name:
                    self.generate_dialog_audio(character_name)

                another = input("\nGenerate audio for another character? (y/n): ").strip().lower()
                if another != 'y':
                    break
                continue

            # Double-asset mode
            double_asset_num = base_num + 1  # Position of DOUBLE-ASSET in menu
            if choice == str(double_asset_num):
                print("\n--- Double-Asset Mode ---\n")

                # Ask for asset type with number selection
                print("Select asset type for double generation:")
                asset_types_list = list(self.ASSET_TYPES.keys())
                for i, atype in enumerate(asset_types_list, 1):
                    print(f"  {i}. {atype.upper()}")

                asset_choice = input(f"\nSelect type (1-{len(asset_types_list)}): ").strip()

                try:
                    asset_type = asset_types_list[int(asset_choice) - 1]
                except (ValueError, IndexError):
                    print("Invalid choice!")
                    continue

                # Get descriptions
                base_description = input("\nBase description: ").strip()
                if not base_description:
                    print("Base description cannot be empty!")
                    continue

                variation_description = input("Variation description: ").strip()
                if not variation_description:
                    print("Variation description cannot be empty!")
                    continue

                # Ask for shared traits for better consistency
                print("\n💡 For best consistency, describe shared characteristics:")
                print("   Examples: 'front view, centered', 'wooden texture', 'same angle'")
                shared_traits = input("Shared traits (optional, press Enter to skip): ").strip()

                # Get names
                base_name = input("\nBase name: ").strip()
                if not base_name:
                    base_name = base_description.split()[0] + "_base"

                variation_name = input("Variation name: ").strip()
                if not variation_name:
                    variation_name = base_description.split()[0] + "_variant"

                # Get size (shared between both)
                default_dimensions = self.config.get('dimensions', {}).get(asset_type, [1024, 1024])
                default_width, default_height = default_dimensions

                size_input = input(f"\nSize in pixels [WIDTHxHEIGHT] (default={default_width}x{default_height}, press Enter to use default): ").strip()
                width, height = None, None
                if size_input:
                    try:
                        width, height = map(int, size_input.lower().split('x'))
                        print(f"Using custom size: {width}x{height}")
                    except ValueError:
                        print(f"Invalid format. Using default: {default_width}x{default_height}")

                # Background removal (shared between both)
                remove_bg = None
                if asset_type in ['room', 'door']:
                    bg_choice = input("Remove background? (y/n, default=n): ").strip().lower()
                    remove_bg = bg_choice == 'y'
                elif asset_type in ['npc', 'item']:
                    bg_choice = input("Remove background? (y/n, default=y): ").strip().lower()
                    if bg_choice == 'n':
                        remove_bg = False

                # Generate both assets
                self.generate_double_asset(asset_type, base_description, variation_description,
                                          base_name, variation_name, shared_traits,
                                          remove_bg, width, height)

                another = input("\nGenerate another asset? (y/n): ").strip().lower()
                if another != 'y':
                    break
                continue  # Skip normal single-asset logic

            # Single asset mode
            try:
                asset_type = list(self.ASSET_TYPES.keys())[int(choice) - 1]
            except (ValueError, IndexError):
                print("Invalid choice!")
                continue

            description = input(f"\nDescribe your {asset_type} (e.g., 'friendly shopkeeper with apron'): ").strip()
            if not description:
                continue

            name = input(f"Name for the asset file (e.g., 'shopkeeper'): ").strip()
            if not name:
                name = description.split()[0]

            # Get default dimensions from config
            default_dimensions = self.config.get('dimensions', {}).get(asset_type, [1024, 1024])
            default_width, default_height = default_dimensions

            # Ask for dimensions with default
            size_input = input(f"Size in pixels [WIDTHxHEIGHT] (default={default_width}x{default_height}, press Enter to use default): ").strip()
            width, height = None, None
            if size_input:
                try:
                    width, height = map(int, size_input.lower().split('x'))
                    print(f"Using custom size: {width}x{height}")
                except ValueError:
                    print(f"Invalid format. Using default: {default_width}x{default_height}")

            # Ask about background removal for rooms/doors
            remove_bg = None
            if asset_type in ['room', 'door']:
                bg_choice = input("Remove background? (y/n, default=n): ").strip().lower()
                remove_bg = bg_choice == 'y'
            elif asset_type in ['npc', 'item']:
                bg_choice = input("Remove background? (y/n, default=y): ").strip().lower()
                if bg_choice == 'n':
                    remove_bg = False

            print(f"\nGenerating {asset_type}...")
            self.generate_asset(asset_type, description, name, remove_bg, width, height)

            another = input("\nGenerate another asset? (y/n): ").strip().lower()
            if another != 'y':
                break


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate game assets using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate an NPC
  python tools/asset_generator.py npc "elderly professor with glasses" professor

  # Generate a room with custom size
  python tools/asset_generator.py room "ancient library" library --width 1920 --height 1080

  # Generate an item
  python tools/asset_generator.py item "golden key with ornate design" key_ornate

  # Generate a door
  python tools/asset_generator.py door "heavy wooden door with iron hinges" door_main

  # Interactive mode (asks for size)
  python tools/asset_generator.py --interactive

  # Generate dialog audio for a character
  python tools/asset_generator.py --generate-audio librarian

  # List templates
  python tools/asset_generator.py --list-templates
        """
    )

    parser.add_argument('asset_type', nargs='?', choices=['npc', 'room', 'item', 'door'],
                       help='Type of asset to generate')
    parser.add_argument('description', nargs='?', help='Description of the asset')
    parser.add_argument('name', nargs='?', help='Name for the asset file')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--no-bg-removal', action='store_true',
                       help='Disable background removal')
    parser.add_argument('--width', type=int, help='Image width in pixels (overrides config)')
    parser.add_argument('--height', type=int, help='Image height in pixels (overrides config)')
    parser.add_argument('--list-templates', action='store_true',
                       help='List available templates')
    parser.add_argument('--check-usage', action='store_true',
                       help='Check current usage')
    parser.add_argument('--generate-audio', metavar='CHARACTER',
                       help='Generate audio for character dialog (e.g., librarian)')

    args = parser.parse_args()

    generator = AssetGenerator()

    if args.generate_audio:
        generator.generate_dialog_audio(args.generate_audio, skip_confirmation=True)
        return

    if args.check_usage:
        generator.check_usage_limit()
        return

    if args.list_templates:
        generator.list_templates()
        return

    if args.interactive:
        generator.interactive_mode()
        return

    if not args.asset_type or not args.description:
        parser.print_help()
        return

    name = args.name or args.description.split()[0]
    remove_bg = None if not args.no_bg_removal else False

    generator.generate_asset(args.asset_type, args.description, name, remove_bg, args.width, args.height)


if __name__ == "__main__":
    main()
