import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


def call_ollama(prompt: str) -> dict:
    """Call Ollama local LLM via HTTP API (faster than CLI)"""
    
    # Use Ollama's REST API for faster response
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 4096,  # Max tokens to generate
            }
        },
        timeout=300  # 5 minute timeout
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"Ollama error: {response.text}")
    
    result = response.json()
    content = result.get("response", "").strip()
    
    # Clean up response (remove markdown code blocks if present)
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    # Try to find JSON in the response
    json_start = content.find('{')
    json_end = content.rfind('}')
    
    if json_start != -1 and json_end != -1:
        content = content[json_start:json_end + 1]
    
    return json.loads(content)


def call_llm(prompt: str) -> dict:
    """
    Call the configured LLM provider.
    Provider is determined by LLM_PROVIDER env variable.
    """
    if LLM_PROVIDER == "ollama":
        return call_ollama(prompt)
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}. Use 'ollama'.")
