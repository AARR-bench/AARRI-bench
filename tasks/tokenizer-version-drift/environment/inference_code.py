#!/usr/bin/env python3
"""
Inference script for Llama-2-7b-chat.
Used for both old and new environments (same code, different transformers version).
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def generate_response(prompt: str, model_path: str = "meta-llama/Llama-2-7b-chat-hf"):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, device_map="auto"
    )

    # Tokenize with padding (used for batched inference)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512,
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        do_sample=False,
        temperature=1.0,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


if __name__ == "__main__":
    print(generate_response("What is the capital of France?"))
