#!/usr/bin/env python3
"""
Asset Generator for Point & Click Adventure Game Engine
Generates game assets (NPCs, Rooms, Items, Doors, Actions) using AI image generation.
"""

import os
import sys
import argparse
import yaml
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import base64

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
        'door': 'assets/doors',
        'action': 'assets/actions'
    }

    def __init__(self, config_path: str = "tools/config.yaml", style_config_path: str = "tools/style_config.yaml"):
        """Initialize the asset generator."""
        self.config_path = Path(config_path)
        self.style_config_path = Path(style_config_path)
        self.config = self._load_config()
        self.style_config = self._load_style_config()
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

        # Background handling
        if asset_type in ['npc', 'item', 'action']:
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
                                   width: int = None, height: int = None) -> Optional[bytes]:
        """Generate image using Hugging Face Inference API (FREE!).

        Args:
            prompt: Positive prompt
            negative_prompt: Negative prompt
            asset_type: Type of asset (for default dimensions)
            width: Override width (None = use config)
            height: Override height (None = use config)
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

            # Generate image using SDK
            image = self.hf_client.text_to_image(
                prompt=full_prompt,
                model=model,
                width=width,
                height=height,
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
                                width: int = None, height: int = None) -> Optional[bytes]:
        """Generate image using Stability AI API (LIMITED FREE TIER).

        Args:
            prompt: Positive prompt
            negative_prompt: Negative prompt
            asset_type: Type of asset (for default dimensions)
            width: Override width (None = use config)
            height: Override height (None = use config)
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

        print(f"Generating with style: {self.style_config.get('master_style', {}).get('art_style', 'default')}")
        print(f"Provider: Stability AI (Limited free tier)")
        print(f"Size: ~{width}x{height} (aspect ratio: {aspect_ratio})")
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
                      width: int = None, height: int = None) -> Optional[bytes]:
        """Generate image using configured provider.

        Args:
            prompt: Positive prompt
            negative_prompt: Negative prompt
            asset_type: Type of asset (for default dimensions)
            width: Override width (None = use config)
            height: Override height (None = use config)
        """
        provider = self.config.get('provider', 'huggingface').lower()

        if provider == 'huggingface' or provider == 'hf':
            return self.generate_image_huggingface(prompt, negative_prompt, asset_type, width, height)
        elif provider == 'stability' or provider == 'stabilityai':
            return self.generate_image_stability(prompt, negative_prompt, asset_type, width, height)
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
                      remove_bg: bool = None, width: int = None, height: int = None) -> Optional[Path]:
        """Generate a single asset.

        Args:
            asset_type: Type of asset (npc, room, item, door)
            description: Text description of the asset
            name: Filename for the asset
            remove_bg: Override background removal setting (None = use config)
            width: Override width (None = use config default)
            height: Override height (None = use config default)
        """
        if not self.check_usage_limit():
            return None

        # Build prompt with style configuration
        positive_prompt, negative_prompt = self.build_prompt(asset_type, description)

        # Generate image with optional size override
        image_data = self.generate_image(positive_prompt, negative_prompt, asset_type, width, height)
        if not image_data:
            return None

        # Remove background based on config (unless explicitly overridden)
        if remove_bg is None:
            # Check config for this asset type
            bg_config = self.config.get('remove_background', {})
            remove_bg = bg_config.get(asset_type, asset_type in ['npc', 'item', 'action'])

        if remove_bg:
            image_data = self.remove_background(image_data)

        # Save asset
        filepath = self.save_asset(image_data, asset_type, name)
        return filepath

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
            ],
            'action': [
                ('lever', 'Mechanical lever or switch'),
                ('button', 'Push button or pressure plate'),
                ('statue', 'Interactive statue or monument'),
                ('chest', 'Treasure chest or container'),
                ('fountain', 'Decorative fountain'),
                ('altar', 'Ritual altar or shrine'),
                ('telescope', 'Viewing telescope or spyglass'),
                ('throne', 'Royal throne or seat'),
            ],
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
            print("\nAsset Types:")
            for i, atype in enumerate(self.ASSET_TYPES.keys(), 1):
                print(f"  {i}. {atype.upper()}")
            print(f"  {len(self.ASSET_TYPES) + 1}. Exit")

            choice = input(f"\nSelect asset type (1-{len(self.ASSET_TYPES) + 1}): ").strip()

            if choice == str(len(self.ASSET_TYPES) + 1):
                print("Goodbye!")
                break

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
            elif asset_type in ['npc', 'item', 'action']:
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

  # Generate an action object
  python tools/asset_generator.py action "ancient stone lever" lever

  # Interactive mode (asks for size)
  python tools/asset_generator.py --interactive

  # List templates
  python tools/asset_generator.py --list-templates
        """
    )

    parser.add_argument('asset_type', nargs='?', choices=['npc', 'room', 'item', 'door', 'action'],
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

    args = parser.parse_args()

    generator = AssetGenerator()

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
