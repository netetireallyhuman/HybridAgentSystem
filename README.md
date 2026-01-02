# Hybrides Agentensystem – Erste Schritte

Dieses Projekt umfasst meine ersten Schritte bei der Einrichtung eines hybriden Agentensystems mit lokalen und Cloud-basierten KI-Modellen.
Hierin sind nur funktionierende getestete Zugriffe enthalten.

<small>Datei: ...\AI\Agent_System\ReadMe!.md</small>  
<small>Stand: 02.01.2026</small>
<small>Autor: [Erik Nagel](https://github.com/netetireallyhuman)</small>

---

## Inhaltsverzeichnis
1. [Ollama KI-Client](#ollama-ki-client)
2. [Python KI-Zugriffe](#python-ki-zugriffe)
3. [Sourcecodes](#sourcecodes)
4. [Modellübersicht](#modellübersicht)

---

## Ollama KI-Client

### Installation
1. **Ollama herunterladen und installieren:**
   - [Download Ollama](https://ollama.com/download)
   - Installation durchführen.

2. **Umgebungsvariable erstellen:**
   - Eine neue Umgebungsvariable mit dem Namen `OLLAMA_MODELS` erstellen.
   - Als Wert den Pfad zum gewünschten Speicherort der Modelle angeben.

3. **Modelle herunterladen:**
   - Modelle können direkt über den Ollama KI-Client oder über die Kommandozeile heruntergeladen werden.
   - Beispiel: `ollama pull deepseek-r1:7b`

4. **Installation überprüfen:**
   - `ollama list` – Zeigt alle heruntergeladenen Modelle an.
   - `ollama ps` – Zeigt die Modelle, auf die kürzlich zugegriffen wurde.

5. **Kommandozeilen-Tests (optional):**
   - `ollama run deepseek-r1` – Startet das Modell für Tests.

---

## Python KI-Zugriffe

### Projektstruktur
```
Agent_System
├─config
│   └─llm_config.py
├─tools
│   ├─duckduckgo_client.py
│   ├─gemini_client.py
│   └─[openai_client.py]
└─agents
    └─ollama_client.py
```

### Einrichtung
1. **Projektordner erstellen:**
   - Einen neuen Ordner, z.B. `Agent_System`, anlegen und mit VSCode öffnen.

2. **Unterordner anlegen:**
   - `config`, `tools`, `agents`

3. **Virtuelle Umgebung erstellen:**
   ```bash
   python -m venv myvenv/
   ```

4. **Virtuelle Umgebung aktivieren:**
   ```bash
   .\myvenv\Scripts\activate.ps1
   ```

5. **Python-Interpreter auswählen:**
   - In VSCode: `Strg+Umschalt+P` → `Python: Select Interpreter`
   - `myvenv (3.14.2) .\myvenv\Scripts\python.exe` auswählen

6. **Debugger konfigurieren:**
   - `Run/Add Configuration` → Debug-Konfiguration hinzufügen:
   ```json
   {
       "configurations": [
           {
               "name": "Python Debugger: Current File",
               "type": "debugpy",
               "request": "launch",
               "program": "${file}",
               "console": "integratedTerminal",
               "env": {
                   "PYTHONPATH": "${workspaceFolder}"
               }
           }
       ]
   }
   ```

7. **Abhängigkeiten installieren:**
   ```bash
   python -m pip install --upgrade pip
   pip install pyautogen
   pip install openai
   pip install google-genai
   pip install ddgs
   [ggf. für openai_client.py: pip install "autogen-ext[openai]"]
   ```

8. **Tests durchführen:**
   - `agents/ollama_client.py` – Testet das lokal laufende Meta-LLM.  
      <small>Ausgabe: Ich bin Gemma, ein großes Sprachmodell, das von Google DeepMind trainiert wurde.
      Ich bin ein Open-Weights-Modell, das öffentlich verfügbar ist.
      Ich kann Text und Bilder als Eingabe nehmen und nur Text ausgeben.</small>
   - `tools/gemini_client.py` – Testet das online laufende Google-LLM.
      <small>Ausgabe: AI lets computers learn from data to recognize patterns and make decisions.</small>
   - `tools/duckduckgo_client.py` – Testet die Websuche über DuckDuckGo.
      <small>Ausgabe:  
        ...  
           "title": "Einwohnerbestand Berlin - Grunddaten",  
           "href": "https://www.statistik-berlin-brandenburg.de/a-i-5-hj",  
           "body": "Berliner Einwohnerbestand wächst weiter. Berlin zählte am 30. Juni 2025 insgesamt 3.902.645 Einwohnerinnen und Einwohner und verzeichnet gegenüber dem Vorjahr einen Zuwachs von 5.500 Personen. Die Zahl an Ausländerinnen und Ausländern war um 836 Personen auf 971.042 gesunken."  
      ...</small>
   - Ggf. `tools/openai_client.py` – Testet das online laufende OpenAI-LLM.
      <small>Ausgabe: Exception has occurred: RateLimitError  
      Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details.  
      ...  
      Der Fehler ist plausibel, da das Modell aktuell kostenpflichtig ist
      und ich nichts bezahlen möchte.</small>

9. **Abhängigkeiten speichern:**
   ```bash
   pip freeze > requirements.txt
   ```

---

## Sourcecodes

### llm_config.py
```python
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
```

### ollama_client.py
```python
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
```

### gemini_client.py
```python
# gemini_client.py
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text) # type: ignore
```

### duckduckgo_client.py
```python
# duckduckgo_client.py
from ddgs import DDGS # type: ignore
import json

def search_web(query: str, max_results: int = 3) -> str:
    """
    Führt eine DuckDuckGo-Web-Suche durch.
    Gibt ein JSON-formatiertes Ergebnis zurück.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Fehler bei der Suche: {str(e)}"

if __name__ == "__main__": # nur ausführen, wenn das Programm direkt ausgeführt wird und nicht über import als Modul geladen wurde
    print("🔍 Teste Web-Suche mit DuckDuckGo...\n")
    
    # Beispiel-Suche
    test_query = "aktuelle Bevölkerung von Berlin 2025"
    print(f"Suche: '{test_query}'\n")
    
    result = search_web(test_query, max_results=2)
    print("Ergebnis:")
    print(result)
    print("\n✅ Test abgeschlossen.")
```

---

### openai_client.py
```python
# openai_client.py
# pip install pyautogen
# pip install "autogen-ext[openai]"
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
async def main() -> None:
    agent = AssistantAgent("assistant", OpenAIChatCompletionClient(model="gpt-4o"))
    print(await agent.run(task="Say 'Hello World!'"))

asyncio.run(main())
```

## Modellübersicht

| Modell               | Größe (Parameter) | Benötigter VRAM (ca.) | Hardware-Klasse                     |
|----------------------|-------------------|-----------------------|--------------------------------------|
| gpt-oss:120b         | 120 Mrd.          | ~70-80 GB             | High-End Workstation (z.B. 4x RTX 4090) |
| qwen3-coder:30b      | 30 Mrd.           | ~20-24 GB             | Enthusiast (z.B. RTX 3090 / 4090)     |
| qwen3:30b            | 30 Mrd.           | ~20-24 GB             | Enthusiast (z.B. RTX 3090 / 4090)     |
| qwen3-vl:30b         | 30 Mrd.           | ~22-26 GB             | Enthusiast (Grafikkarte mit viel VRAM) |
| gemma3:27b           | 27 Mrd.           | ~18-22 GB             | Oberklasse (RTX 3090 / 4090)         |
| gpt-oss:20b          | 20 Mrd.           | ~14-16 GB             | Mittelklasse (RTX 3080 16GB / 4070 Ti Super) |
| gemma3:12b           | 12 Mrd.           | ~8-10 GB              | Mittelklasse (RTX 3060 12GB / 4070)  |
| deepseek-r1:8b       | 8 Mrd.            | ~6-8 GB               | Standard PC (RTX 3060 / 4060)        |
| qwen3-vl:8b          | 8 Mrd.            | ~6-8 GB               | Standard PC                          |
| qwen3:8b             | 8 Mrd.            | ~6-8 GB               | Standard PC                          |
| llama3:8b            | 8 Mrd.            | ~6-8 GB               | Standard PC                          |
| deepseek-r1:7b       | 7 Mrd.            | ~5-6 GB               | Einsteiger / Laptop                  |
| gemma3:4b            | 4 Mrd.            | ~3-4 GB               | Einsteiger / Laptop                  |
| qwen3-vl:4b          | 4 Mrd.            | ~3-4 GB               | Einsteiger / Laptop                  |
| qwen3:4b             | 4 Mrd.            | ~3-4 GB               | Einsteiger / Laptop                  |
| gemma3:1b            | 1 Mrd.            | ~1-2 GB               | Läuft fast überall                   |

---
