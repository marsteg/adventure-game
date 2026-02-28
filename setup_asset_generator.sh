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

# Check current NumPy version
echo ""
echo "Checking NumPy version..."
NUMPY_VERSION=$(python3 -c "import numpy; print(numpy.__version__)" 2>/dev/null)
if [ $? -eq 0 ]; then
    NUMPY_MAJOR=$(echo $NUMPY_VERSION | cut -d. -f1)
    echo "Current NumPy version: $NUMPY_VERSION"

    if [ "$NUMPY_MAJOR" -ge 2 ]; then
        echo ""
        echo "⚠️  NumPy 2.x detected - this is incompatible with rembg"
        echo "   Downgrading to NumPy 1.x for compatibility..."
        pip3 install 'numpy<2' || {
            echo "❌ Failed to downgrade NumPy"
            exit 1
        }
        echo "✓ NumPy downgraded to 1.x"
    else
        echo "✓ NumPy 1.x already installed (compatible)"
    fi
else
    echo "NumPy not installed - will be installed with dependencies"
fi

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
