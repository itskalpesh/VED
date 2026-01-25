from llama_cpp import Llama
import os
from config.config import DEBUG

MODEL_PATH = "models/qwen2.5-3b-instruct-q5_0.gguf"
_llm = None

def get_llm():
    global _llm
    if not os.path.exists(MODEL_PATH):
        if DEBUG: print(f"[OFFLINE] Model not found at {MODEL_PATH}")
        return None
    
    if _llm is None:
        _llm = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)
    return _llm

def offline_generate(text, recall):
    llm = get_llm()
    if not llm: return "Local model file is missing."

    name = recall.get("user_name", "User")
    prompt = f"<|system|>\nYou are VED. User is {name}.\n<|user|>\n{text}\n<|assistant|>\n"

    output = llm(
        prompt, 
        max_tokens=512, 
        stop=["<|user|>", "<|system|>", "User:"], 
        echo=False
    )
    return output["choices"][0]["text"].strip()