"""
Simple test script to verify Llama 3.2 3B local loading works.
"""
import sys
sys.path.insert(0, '.')

from local_models import LocalHuggingFace
from loggers import logger

def test_local_model():
    """Test that we can load and generate with Llama 3.2 locally."""
    print("="*70)
    print("Testing Llama 3.2 3B Local Loading")
    print("="*70)

    # Initialize model
    print("\n1. Loading model...")
    model = LocalHuggingFace("llama-3.2-3b-instruct")
    print("✓ Model loaded successfully!")

    # Test conversation formatting
    print("\n2. Testing conversation formatting...")
    test_conv = [
        {"role": "user", "content": "Hello! What is 2+2?"}
    ]
    formatted = model.format_conversation(test_conv)
    print(f"Formatted prompt:\n{formatted}")

    # Test generation
    print("\n3. Testing generation...")
    test_convs = [
        [
            {"role": "user", "content": "What is the capital of France?"}
        ],
        [
            {"role": "user", "content": "Write a haiku about programming."}
        ]
    ]

    responses = model.batched_generate(
        convs_list=test_convs,
        max_n_tokens=50,
        temperature=0.7,
        top_p=0.9
    )

    print("\nGenerated responses:")
    for i, response in enumerate(responses, 1):
        print(f"\nPrompt {i}: {test_convs[i-1][0]['content']}")
        print(f"Response {i}: {response}")

    print("\n" + "="*70)
    print("✓ All tests passed! Llama 3.2 is ready to use.")
    print("="*70)


if __name__ == "__main__":
    # Set logger verbosity
    logger.set_level(2)
    test_local_model()
