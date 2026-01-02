# llm_config.py
LLM_CONFIG_OLLAMA: dict[str, list[dict[str, str]] | float] = {
    "config_list": [
        {
            "model": "gemma3:4b",
            # "model": "deepseek-r1:7b",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",  # Pflichtfeld, wird ignoriert
        }
    ],
    "temperature": 0.7,
}
