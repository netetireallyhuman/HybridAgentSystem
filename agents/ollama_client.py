# ollama_client.py
import openai
from config.llm_config import LLM_CONFIG_OLLAMA

config_list = LLM_CONFIG_OLLAMA.get("config_list", [])
if not config_list:
    raise ValueError("config_list ist leer")
cfg = config_list[0] # type: ignore

model: str = cfg.get("model") # type: ignore
base_url: str = cfg.get("base_url") # type: ignore
api_key: str = cfg.get("api_key") # type: ignore
temperature: float = LLM_CONFIG_OLLAMA.get("temperature", 0.0) # type: ignore

client = openai.OpenAI(
    base_url=base_url,
    api_key=api_key
)

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Hallo, wer bist du?"}],
    temperature=temperature
)

print(response.choices[0].message.content)