# ollama_client.py
# pip install pyautogen
# pip install "autogen-ext[openai, ollama]"
import openai

# Define the model and base URL
model_name = "gemma3:4b"
base_url = "http://localhost:11434/v1"

# Create the OpenAI client
client = openai.OpenAI(
    base_url=base_url,
    api_key="ollama" # Ollama ignores the api_key-value for the local AI, but expects it to be present.
)

# Create the prompt
prompt = "Hallo, wer bist du?"

# Send the prompt to the OpenAI API
# The model and temperature are passed directly to the create method.
# What does temperature do?
# Low values ​​(e.g., 0.0–0.5):
# The model selects the most likely words more deterministically. The answers are more consistent
# but less creative (Good for facts, code, and formal texts).
# High values ​​(e.g., 0.8–1.5):
# The model selects more randomly from a wider range of words. The answers are more creative
# but also more unpredictable and prone to errors (Brainstorming, creative writing, and dialogues).
# Default value: Usually 1.0 (balanced mix).

response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

# Print the response
print(response.choices[0].message.content)
