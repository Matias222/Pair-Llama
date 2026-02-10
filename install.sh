#!/bin/bash
# Clean installation script for PAIR with Llama 3.2

set -e  # Exit on error

echo "=========================================="
echo "PAIR Installation for Llama 3.2"
echo "=========================================="
echo ""

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠ WARNING: Not in a virtual environment!"
    echo "It's recommended to use a venv. Create one with:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo ""
    read -p "Continue anyway? [y/N]: " continue_install
    if [[ ! $continue_install =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Step 1: Upgrading pip and base tools..."
pip install --upgrade pip setuptools wheel

echo ""
echo "Step 2: Uninstalling conflicting packages..."
pip uninstall -y jailbreakbench litellm || true

echo ""
echo "Step 3: Installing requirements..."
pip install -r requirements.txt

echo ""
echo "Step 4: Verifying installation..."
python -c "import litellm; print(f'✓ litellm version: {litellm.__version__}')"
python -c "import transformers; print(f'✓ transformers version: {transformers.__version__}')"
python -c "import torch; print(f'✓ torch version: {torch.__version__}')"

echo ""
echo "=========================================="
echo "✓ Installation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-key'"
echo ""
echo "2. Disable wandb:"
echo "   export WANDB_MODE=disabled"
echo ""
echo "3. Test the installation:"
echo "   python test_llama32.py"
echo ""
