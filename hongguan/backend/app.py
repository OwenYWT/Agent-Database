from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

# Load your model at startup
model_name = "/home/yzhao862/MemGPT/Llama-3.3-70B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_8bit=True,
    device_map="auto",
    trust_remote_code=True
)

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 50
    temperature: float = 0.7

@app.post("/v1/completions")
def generate_completion(request: CompletionRequest):
    inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature
        )
    completion_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return {"completion": completion_text}
