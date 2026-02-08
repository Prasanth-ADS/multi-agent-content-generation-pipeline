"""
Test script to run Phi-3-mini locally using transformers.

Requirements:
- Python 3.9+
- pip install transformers torch accelerate

Note: First run will download ~7GB model files.
If no GPU, it will run on CPU (very slow for 7B models).
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("🔌 Loading Phi-3-mini model locally...")
print("📦 This will download ~7GB on first run...\n")

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️  Using device: {device}")
if device == "cpu":
    print("⚠️  Warning: CPU-only mode will be very slow for 7B models\n")

# Load model and tokenizer
print("📥 Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct", 
    trust_remote_code=True
)

print("📥 Loading model (this may take a while)...")
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct", 
    trust_remote_code=True,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    device_map="auto" if device == "cuda" else None
)

# If CPU, move model to CPU
if device == "cpu":
    model = model.to("cpu")

print("✅ Model loaded!\n")

# Prepare messages
messages = [
    {"role": "user", "content": "Who are you?"},
]

print("🔄 Generating response...")

# Tokenize with chat template
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

# Generate
outputs = model.generate(
    **inputs, 
    max_new_tokens=100,
    temperature=0.7,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

# Decode response (skip the input tokens)
response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)

print("\n" + "="*50)
print("💬 Response:")
print("="*50)
print(response)
print("="*50)
print("\n✅ Test complete!")
