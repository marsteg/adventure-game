#!/bin/bash
# Quick setup script for asset generator

echo "=== Asset Generator Setup ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi
echo "✓ Python 3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r tools/requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

# Setup config
echo ""
if [ ! -f tools/config.yaml ]; then
    cp tools/config.yaml.example tools/config.yaml
    echo "✓ Created tools/config.yaml"
    echo ""
    echo "⚠️  ACTION REQUIRED:"
    echo "   1. Get your free API key from https://platform.stability.ai/"
    echo "   2. Edit tools/config.yaml"
    echo "   3. Replace 'your-api-key-here' with your actual API key"
    echo ""
else
    echo "✓ tools/config.yaml already exists"
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "  1. Get API key: https://platform.stability.ai/"
echo "  2. Add key to: tools/config.yaml"
echo "  3. Run: python3 tools/asset_generator.py --interactive"
echo ""
echo "For more info, see: tools/README.md"
