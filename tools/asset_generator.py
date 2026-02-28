#!/usr/bin/env python3
"""
Asset Generator for Point & Click Adventure Game Engine
Generates game assets (NPCs, Rooms, Items, Doors) using AI image generation.
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

    def __init__(self, config_path: str = "tools/config.yaml"):
        """Initialize the asset generator."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.prompts = self._load_prompts()
        self.usage_file = Path("tools/.usage_tracker.json")
        self.usage = self._load_usage()

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            print(f"Config file not found at {self.config_path}")
            print("Please copy config.yaml.example to config.yaml and add your API key.")
            sys.exit(1)

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_prompts(self) -> Dict:
        """Load prompt templates."""
        prompts = {}
        prompts_dir = Path("tools/prompts")

        for asset_type in self.ASSET_TYPES.keys():
            prompt_file = prompts_dir / f"{asset_type}_prompts.yaml"
            if prompt_file.exists():
                with open(prompt_file, 'r') as f:
                    prompts[asset_type] = yaml.safe_load(f)

        return prompts

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

        print(f"Monthly usage: {self.usage['count']}/{limit} (Remaining: {remaining})")

        if self.usage["count"] >= limit:
            print("⚠️  Monthly limit reached! Wait until next month or upgrade your plan.")
            return False
        return True

    def build_prompt(self, asset_type: str, description: str) -> str:
        """Build a complete prompt for the asset type."""
        style_guide = self.prompts.get(asset_type, {}).get('style_guide', '')

        if asset_type == 'npc' or asset_type == 'item':
            # NPCs and items need transparent backgrounds
            bg_instruction = ", transparent background, isolated on white"
        else:
            bg_instruction = ""

        full_prompt = f"{description}, {style_guide}{bg_instruction}"
        return full_prompt.strip()

    def generate_image_stability(self, prompt: str, asset_type: str) -> Optional[bytes]:
        """Generate image using Stability AI API."""
        api_key = self.config.get('stability_api_key')
        if not api_key or api_key == 'your-api-key-here':
            print("Error: Please set your Stability AI API key in config.yaml")
            print("Get a free API key at: https://platform.stability.ai/")
            return None

        # Use Stable Diffusion 3.5 Large (free tier compatible)
        url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

        headers = {
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        }

        # Negative prompt for better quality
        negative_prompt = "blurry, low quality, distorted, disfigured, ugly, bad anatomy"

        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": "1:1",
            "output_format": "png",
            "mode": "text-to-image"
        }

        print(f"Generating image with prompt: {prompt}")
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
                      remove_bg: bool = None) -> Optional[Path]:
        """Generate a single asset."""
        if not self.check_usage_limit():
            return None

        # Build prompt
        prompt = self.build_prompt(asset_type, description)

        # Generate image
        image_data = self.generate_image_stability(prompt, asset_type)
        if not image_data:
            return None

        # Remove background for NPCs and items (unless disabled)
        if remove_bg is None:
            remove_bg = asset_type in ['npc', 'item']

        if remove_bg:
            image_data = self.remove_background(image_data)

        # Save asset
        filepath = self.save_asset(image_data, asset_type, name)
        return filepath

    def list_templates(self, asset_type: Optional[str] = None):
        """List available prompt templates."""
        if asset_type:
            templates = self.prompts.get(asset_type, {}).get('templates', [])
            print(f"\n{asset_type.upper()} Templates:")
            for template in templates:
                print(f"  - {template['name']}: {template['description']}")
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
            print("  5. Exit")

            choice = input("\nSelect asset type (1-5): ").strip()

            if choice == '5':
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

            # Ask about background removal for rooms/doors
            remove_bg = None
            if asset_type in ['room', 'door']:
                bg_choice = input("Remove background? (y/n, default=n): ").strip().lower()
                remove_bg = bg_choice == 'y'

            print(f"\nGenerating {asset_type}...")
            self.generate_asset(asset_type, description, name, remove_bg)

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

  # Generate a room
  python tools/asset_generator.py room "ancient library with mystical books" library_ancient

  # Generate an item
  python tools/asset_generator.py item "golden key with ornate design" key_ornate

  # Interactive mode
  python tools/asset_generator.py --interactive

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

    generator.generate_asset(args.asset_type, args.description, name, remove_bg)


if __name__ == "__main__":
    main()
