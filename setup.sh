#!/bin/bash
# Setup script for PAIR with Llama 3.2 support

echo "=========================================="
echo "PAIR Setup for Llama 3.2 3B"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "✗ Installation failed!"
    exit 1
fi

echo ""
echo "✓ Dependencies installed successfully!"
echo ""

# Check if model exists
MODEL_PATH="/home/matias-avendano/Desktop/tesis/modelos/Llama-3.2-3B-Instruct"
if [ -d "$MODEL_PATH" ]; then
    echo "✓ Llama 3.2 model found at: $MODEL_PATH"
else
    echo "⚠ WARNING: Llama 3.2 model not found at: $MODEL_PATH"
    echo "Please update LLAMA_32_PATH in config.py"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-key-here'"
echo ""
echo "2. Test the setup:"
echo "   python test_llama32.py"
echo ""
echo "3. Generate attacks:"
echo "   python run_pair_llama32.py"
echo ""
