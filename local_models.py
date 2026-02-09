"""
Local model loading for HuggingFace transformers.
Supports running models locally without API calls.
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import HF_MODEL_NAMES, LITELLM_TEMPLATES, Model
from loggers import logger


class LocalHuggingFace:
    """Local HuggingFace model loader for Llama 3.2 and other models."""

    def __init__(self, model_name: str):
        """
        Initialize local HuggingFace model.

        Args:
            model_name: Model name from Model enum (e.g., "llama-3.2-3b-instruct")
        """
        self.model_name = Model(model_name)
        self.hf_model_path = HF_MODEL_NAMES[self.model_name]

        logger.info(f"Loading local model from: {self.hf_model_path}")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.hf_model_path,
            trust_remote_code=True,
            use_fast=False
        )

        # Set padding token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        self.tokenizer.padding_side = 'left'

        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.hf_model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )
        self.model.eval()

        # Set EOS tokens from config
        if self.model_name in LITELLM_TEMPLATES:
            self.eos_tokens = LITELLM_TEMPLATES[self.model_name]["eos_tokens"]
            self.post_message = LITELLM_TEMPLATES[self.model_name]["post_message"]
            self.template_config = LITELLM_TEMPLATES[self.model_name]
        else:
            self.eos_tokens = []
            self.post_message = ""
            self.template_config = None

        self.use_open_source_model = True

        logger.info(f"Model loaded successfully on device: {self.model.device}")

    def format_conversation(self, messages: list[dict]) -> str:
        """
        Format conversation messages into a prompt string.

        Args:
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            Formatted prompt string
        """
        if self.template_config is None:
            # Fallback to simple formatting
            prompt = ""
            for msg in messages:
                role = msg['role']
                content = msg['content']
                prompt += f"{role}: {content}\n"
            return prompt

        # Use template config
        prompt = self.template_config["initial_prompt_value"]

        for msg in messages:
            role = msg['role']
            content = msg['content']

            if role in self.template_config["roles"]:
                role_config = self.template_config["roles"][role]
                prompt += role_config["pre_message"]
                prompt += content
                prompt += role_config["post_message"]

        # Add assistant prefix for generation
        if messages[-1]['role'] != 'assistant':
            assistant_config = self.template_config["roles"]["assistant"]
            prompt += assistant_config["pre_message"]

        return prompt

    def batched_generate(
        self,
        convs_list: list[list[dict]],
        max_n_tokens: int,
        temperature: float,
        top_p: float = 1.0,
        extra_eos_tokens: list[str] = None
    ) -> list[str]:
        """
        Generate responses for a batch of conversations.

        Args:
            convs_list: List of conversation message lists
            max_n_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            extra_eos_tokens: Additional stop tokens

        Returns:
            List of generated response strings
        """
        # Format all conversations
        prompts = [self.format_conversation(conv) for conv in convs_list]

        # Tokenize
        inputs = self.tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=2048
        ).to(self.model.device)

        # Prepare stop tokens
        stop_strings = self.eos_tokens.copy() if self.eos_tokens else []
        if extra_eos_tokens:
            stop_strings.extend(extra_eos_tokens)

        # Generate
        with torch.no_grad():
            if temperature < 1e-6:  # Greedy decoding
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_n_tokens,
                    do_sample=False,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            else:
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_n_tokens,
                    do_sample=True,
                    temperature=temperature,
                    top_p=top_p,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )

        # Decode outputs (only new tokens)
        input_lengths = inputs['input_ids'].shape[1]
        responses = []
        for output in outputs:
            generated_ids = output[input_lengths:]
            response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)

            # Remove stop strings if present
            for stop_str in stop_strings:
                if stop_str in response:
                    response = response[:response.index(stop_str)]

            responses.append(response)

        return responses
