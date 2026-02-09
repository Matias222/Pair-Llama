#!/bin/bash
# Quick start script for generating PAIR attacks on Llama 3.2 3B

echo "=========================================="
echo "PAIR Attack Generation for Llama 3.2 3B"
echo "=========================================="
echo ""

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠ WARNING: OPENAI_API_KEY not set!"
    echo "Please set it with: export OPENAI_API_KEY='your-key'"
    echo ""
    read -p "Do you want to use Llama 3.2 as attacker (free but less effective)? [y/N]: " use_local
    if [[ $use_local =~ ^[Yy]$ ]]; then
        ATTACK_MODEL="llama-3.2-3b-instruct"
        echo "Using Llama 3.2 as attacker (no API needed)"
    else
        echo "Exiting. Please set OPENAI_API_KEY first."
        exit 1
    fi
else
    ATTACK_MODEL="gpt-3.5-turbo-1106"
    echo "✓ OpenAI API key found"
    echo "Using GPT-3.5 as attacker"
fi

echo ""
echo "Configuration:"
echo "  Attack Model: $ATTACK_MODEL"
echo "  Target Model: llama-3.2-3b-instruct (local)"
echo "  Streams: 5"
echo "  Iterations: 5"
echo ""

# Disable wandb if not logged in
export WANDB_MODE=disabled

# Option 1: Test the setup
echo "Step 1: Testing Llama 3.2 loading..."
python test_llama32.py

if [ $? -ne 0 ]; then
    echo "✗ Test failed! Please check the error above."
    exit 1
fi

echo ""
echo "✓ Test passed!"
echo ""

# Option 2: Generate attacks
read -p "Do you want to generate PAIR attacks now? [Y/n]: " run_pair

if [[ ! $run_pair =~ ^[Nn]$ ]]; then
    echo ""
    echo "Generating PAIR attacks..."
    echo "This will take approximately 30-60 minutes."
    echo ""

    python run_pair_llama32.py \
        --attack-model "$ATTACK_MODEL" \
        --n-streams 5 \
        --n-iterations 5 \
        --output-dir pair_results \
        --output-csv pair_attacks_llama32.csv

    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✓ PAIR attacks generated successfully!"
        echo "=========================================="
        echo "Results saved to: pair_results/pair_attacks_llama32.csv"
        echo ""
        echo "Next steps:"
        echo "1. Review the generated attacks in pair_results/"
        echo "2. Use them to evaluate your defense with defensa_3.py"
        echo ""
    else
        echo ""
        echo "✗ Attack generation failed. Check the errors above."
    fi
else
    echo "Skipping attack generation."
    echo ""
    echo "To generate attacks manually, run:"
    echo "  python run_pair_llama32.py --attack-model $ATTACK_MODEL"
fi
