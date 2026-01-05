# Hybrides KI-Agentensystem

Dieses Projekt umfasst meine ersten Schritte bei der Einrichtung eines hybriden Agentensystems mit lokalen und Cloud-basierten KI-Modellen.
Die hier enthaltenen Zugriffe sind getestet und funktionieren.
Das Haupt-Script **"agent_team.py"** arbeitet eigenständig. Die Scripte im Ordner "demos" werden hierfür nicht benötigt.

<small>**Wichtiger Hinweis: Falls du später eine Weiterentwicklung planst, berücksichtige bitte unbedingt Sicherheit und Datenschutz!
Schließlich werden lokal Scripte ausgeführt und Web-Recherchen durchgeführt.**</small>


<small>Datei: ...\HybridAgentSystem\README.md</small>  
<small>Stand: 04.01.2026</small>
<small>Autor: [Erik Nagel](https://github.com/netetireallyhuman)</small>

---

## Inhaltsverzeichnis
1. [Ollama KI-Client](#ollama-ki-client)
2. [Gemini KI-Api](#gemini-ki-api)
3. [Python KI-Projekt](#python-ki-Projekt)
4. [Sourcecodes](#sourcecodes)
5. [Konversationsprotokoll](#konversationsprotokoll-python-skript-zur-datumsausgabe)
6. [optionale Sourcecodes](#optionale-sourcecodes)
7. [optionale Tests](#optionale-tests)
8. [Modellübersicht](#modellübersicht)

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
   - Für dieses Beispiel: `ollama pull gemma3:4b`

4. **Installation überprüfen:**
   - `ollama list` – Zeigt alle heruntergeladenen Modelle an.
   - `ollama ps` – Zeigt die Modelle, auf die kürzlich zugegriffen wurde.

5. **Kommandozeilen-Tests <small>(optional, für die Zugriffe im Python KI-Projekt nicht erforderlich)</small>:**
   - `ollama run gemma3:4b` – Startet das Modell für Tests.

---

## Gemini KI-Api

1. **kostenlosen API-Key erstellen und kopieren:**
   - [auf https://aistudio.google.com](https://aistudio.google.com)
   
2. **API-Key einrichten:**
   - Erstelle eine Umgebungsvariable mit dem Namen **"GEMINI_API_KEY"**
     mit deinem kopierten **API-Key** als Wert.

---

## Python KI-Projekt

### Projektstruktur
```
HybridAgentSystem
 ├─agents
 │   └─agent_team.py
 ├─job.txt
 ├─demo_job.txt
 ├─serious_job.txt
 ├──demos
 │   ├─duckduckgo_client.py
 │   ├─gemini_client.py
 │   ├─ollama_client.py
 │   └─[openai_client.py]
 ├─__init__.py
 ├─README.md
 ├─LICENSE
 └─[requirements.txt]
```

### Einrichtung
1. **Projektordner erstellen:**
   - Einen neuen Ordner, z.B. `HybridAgentSystem`, anlegen und mit VSCode öffnen.

2. **Unterordner anlegen:**
   - `agents`, `demos`

3. **Source-Dateien erstellen [siehe Sourcecodes](#sourcecodes):**
   - `agents/agent_team.py`
   - `job.txt`
   - optional:  
   `demos/gemini_client.py`, `demos/duckduckgo_client.py`, `demos/ollama_client.py`, `ggf. demos/openai_client.py`

4. **Virtuelle Umgebung erstellen:**
   ```bash
   python -m venv myvenv/
   Bei Fehlern einfach wiederholen, bis es klappt (evtl. Timing Problem bei pip)
   ```

5. **Virtuelle Umgebung aktivieren:**
   ```bash
   .\myvenv\Scripts\activate.ps1
   ```

6. **Python-Interpreter auswählen:**
   - In VSCode: `Strg+Umschalt+P` → `Python: Select Interpreter`
   - `myvenv (3.14.2) .\myvenv\Scripts\python.exe    Recommended` auswählen

7. **Debugger konfigurieren:**
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

8. **Abhängigkeiten installieren:**
   ```bash
   python -m pip install --upgrade pip
   pip install pyautogen
   pip install openai
   pip install google-genai
   pip install ddgs
   [ggf. für openai_client.py: pip install "autogen-ext[openai]"]
   ```

9. **Test durchführen:**

   `agents/agent_team.py` – Testet das Agentensystem.

   **Ausgaben siehe [Konversationsprotokoll](#konversationsprotokoll-python-skript-zur-datumsausgabe)**

10. **Abhängigkeiten speichern:**
   ```bash
   pip freeze > requirements.txt
   ```

---

## Sourcecodes

### job.txt (demo_job.txt)
Schreibe ein Python-Skript, das das aktuelle Datum ausgibt, führe es aus und analysiere das Ergebnis.

### agent_team.py

```python
# agent_team.py
# This is a standalone demonstration.
# Important: If you are planning further development, please consider the safety aspects!
# For a glimpse of what this approach may be capable, try "serious_job.txt" later.
# pip install pyautogen
# pip install "autogen-ext[openai, ollama]"
import asyncio
import os
import sys
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

def read_job(input_path: str) -> str:
    data: str = ""
    # Reading a text file into a string.
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        sys.exit(f"Datei nicht gefunden: {input_path}")
    return data

async def main():
    # 1. Create the executor (where the code is executed).
    code_executor = LocalCommandLineCodeExecutor(work_dir="tasks")

    # 2. Create the agent that executes the code.
    # This agent does not have a "model_client", but only a "code_executor".
    executor_agent = CodeExecutorAgent(
        "executor_agent",
        code_executor=code_executor
    )

    # 3. Create the local Agent (Ollama).
    # This agent controls the entire agent system.
    local_analyst = AssistantAgent(
        "local_analyst",
        model_client=OllamaChatCompletionClient(
            model="gemma3:4b",
            host="http://localhost:11434",
            model_info=
            {
                "vision": False,
                "function_calling": True, # Gemma 3 supports tools
                "json_output": True,
                "structured_output": True,
                "family": "gemma3",
            }
        )
    )

    # 4. Create the online agent (Gemini via OpenAI-compatible endpoint).
    # This agent is responsible for web research.
    #       4a. You can obtain a free API key from aistudio.google.com.
    #           Set an environment variable named "GEMINI_API_KEY"
    #           to the value of your API key.
    google_api_key: str = os.environ.get('GEMINI_API_KEY') or ""
    web_researcher = AssistantAgent(
        "web_researcher",
        model_client=OpenAIChatCompletionClient(
            model="gemini-2.5-flash",
            api_key=google_api_key,
            model_info={
                "vision": True,                 # Gemini Flash can see images
                "function_calling": True,       # Very strong in tool usage
                "json_output": True,            # Supports JSON mode
                "structured_output": True,      # Supports schema enforcement
                "family": "gemini"              # Important for the correct prompting format
            }
        ),
        system_message="Du bist ein Web-Experte, der neueste Informationen recherchiert."
    )

    # 5. Assemble a team
    team = RoundRobinGroupChat(
        [local_analyst, web_researcher, executor_agent], 
        max_turns=10
    )

    # 6. Define the job.
    # task_todo: str = "Schreibe ein Python-Skript, das das aktuelle Datum ausgibt, führe es aus und analysiere das Ergebnis."
    # Job einlesen
    task_todo: str = read_job("job.txt")

    # 7. Start the task.
    await Console(team.run_stream(task=task_todo))

if __name__ == "__main__":
    asyncio.run(main())

```
---

## Konversationsprotokoll: Python-Skript zur Datumsausgabe  
<small>Die Ausgabe ist für die formatierte Anzeige etwas angepasst worden, kommt aber so ähnlich
auf der Konsole an.</small>

### Kontext und Warnungen

```plaintext
...\HybridAgentSystem\agents\agent_team.py:27: UserWarning: 
Using LocalCommandLineCodeExecutor may execute code on the local machine which can be unsafe. 
For security, it is recommended to use DockerCommandLineCodeExecutor instead. 
To install Docker, visit: https://docs.docker.com/get-docker/
  code_executor = LocalCommandLineCodeExecutor(work_dir="tasks")

...\HybridAgentSystem\agents\agent_team.py:31: UserWarning: 
No approval function set for CodeExecutorAgent. This means code will be executed automatically without human oversight. 
For security, consider setting an approval_func to review and approve code before execution. 
See the CodeExecutorAgent documentation for examples of approval functions.
  executor_agent = CodeExecutorAgent(
```

### Benutzeranfrage

**Benutzer:**
Schreibe ein Python-Skript, das das aktuelle Datum ausgibt, führe es aus und analysiere das Ergebnis.

### Antwort des Local Analyst

**Local Analyst:**
Okay, hier ist ein Python-Skript, das das aktuelle Datum ausgibt, es ausführt und das Ergebnis analysiert:

```python
import datetime

# Aktuelles Datum abrufen
today = datetime.date.today()

# Datum formatieren (optional, aber für eine bessere Lesbarkeit)
formatted_date = today.strftime("%Y-%m-%d")

# Datum ausgeben
print(f"Das aktuelle Datum ist: {formatted_date}")

# Analyse des Ergebnisses
print("
Analyse des Ergebnisses:")
print(f"Typ der Variablen 'today': {type(today)}")
print(f"Typ der Variablen 'formatted_date': {type(formatted_date)}")
print(f"Wert der Variablen 'today': {today}")
print(f"Wert der Variablen 'formatted_date': {formatted_date}")
```

**Ausführung des Skripts:**

Wenn du dieses Skript ausführst, wird folgendes Ergebnis in der Konsole angezeigt (das genaue Datum wird natürlich dem aktuellen Datum entsprechen, wenn du das Skript ausführst):

```plaintext
Das aktuelle Datum ist: 2024-04-29

Analyse des Ergebnisses:
Typ der Variablen 'today': <class 'datetime.date'>
Typ der Variablen 'formatted_date': <class 'str'>
Wert der Variablen 'today': 2024-04-29
Wert der Variablen 'formatted_date': 2024-04-29
```

**Erklärung:**

1. **`import datetime`:** Importiert das `datetime`-Modul, das Klassen für die Arbeit mit Datum und Uhrzeit bereitstellt.
2. **`today = datetime.date.today()`:** Ruft das aktuelle Datum ab und speichert es in der Variablen `today`.
3. **`formatted_date = today.strftime("%Y-%m-%d")`:** Formatiert das Datum in einen String im Format "YYYY-MM-DD".
4. **`print(f"Das aktuelle Datum ist: {formatted_date}")`:** Gibt das formatierte Datum aus.
5. **Analyse des Ergebnisses:** Zeigt den Datentyp und den Wert der Variablen `today` und `formatted_date`.

### Antwort des Web Researchers

**Web Researcher:**
Ausgezeichnet! Das ist ein sehr klares, korrektes und gut strukturiertes Python-Skript, das die Aufgabe perfekt erfüllt. Als Web-Experte kann ich bestätigen, dass dieser Ansatz sowohl standardkonform als auch eine Best Practice für die Handhabung von Datum und Uhrzeit in Python ist, insbesondere im Kontext von Web-Anwendungen.

#### Expertenanalyse und Kontext für Web-Anwendungen

1. **`datetime`-Modul:** Standard und robust für Datums- und Zeitoperationen.
2. **`strftime()` und Formatierung:** Wichtig für die Kommunikation mit dem Frontend und Benutzern.
3. **Typisierung und Analyse:** Gute Programmierpraxis.

#### Erweiterungen und Nächste Schritte (für Web-Anwendungen):

1. **Zeitzonen:** Kritisch in globalen Web-Anwendungen.
2. **Datum/Uhrzeit-Berechnungen:** Addieren/Subtrahieren von Zeitspannen.
3. **Client-Side vs. Server-Side:** Unterschiedliche Handhabung von Datum und Uhrzeit.

**Fazit:** Dein Skript ist ein hervorragendes Beispiel für die grundlegende und korrekte Handhabung von Datumswerten in Python.

### Ausführung und Ergebnis

**Executor Agent:**
```plaintext
Das aktuelle Datum ist: 2026-01-04

Analyse des Ergebnisses:
Typ der Variablen 'today': <class 'datetime.date'>
Typ der Variablen 'formatted_date': <class 'str'>
Wert der Variablen 'today': 2026-01-04
Wert der Variablen 'formatted_date': 2026-01-04
```

### Abschluss

**Local Analyst:** TERMINATE

**Web Researcher:** Vielen Dank für die Bereitstellung dieses Beispiel-Outputs! Das Ergebnis bestätigt genau das, was wir vom Skript erwarten würden.

**Executor Agent:** Das aktuelle Datum ist: 2026-01-04

**Local Analyst:** TERMINATE

**Web Researcher:** Hier ist das ursprüngliche Python-Skript, das das aktuelle Datum ausgibt und analysiert, noch einmal in einem ausführbaren Code-Block:

```python
import datetime

# Aktuelles Datum abrufen
today = datetime.date.today()

# Datum formatieren (optional, aber für eine bessere Lesbarkeit)
formatted_date = today.strftime("%Y-%m-%d")

# Datum ausgeben
print(f"Das aktuelle Datum ist: {formatted_date}")

# Analyse des Ergebnisses
print("
Analyse des Ergebnisses:")
print(f"Typ der Variablen 'today': {type(today)}")
print(f"Typ der Variablen 'formatted_date': {type(formatted_date)}")
print(f"Wert der Variablen 'today': {today}")
print(f"Wert der Variablen 'formatted_date': {formatted_date}")
```

**Executor Agent:**
```plaintext
Das aktuelle Datum ist: 2026-01-04

Analyse des Ergebnisses:
Typ der Variablen 'today': <class 'datetime.date'>
Typ der Variablen 'formatted_date': <class 'str'>
Wert der Variablen 'today': 2026-01-04
Wert der Variablen 'formatted_date': 2026-01-04
```

**Local Analyst:** TERMINATE

---

## optionale Sourcecodes

### serious_job.txt

```
Stelle folgendes Script "ollama_client.py" vom veralteten Parameter-Format
"llm_config.py" auf die aktuelle openai-Version um,
führe es aus und analysiere das Ergebnis.
---
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
---
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
---
```

### ollama_client.py

```python
# ollama_client.py
# pip install pyautogen
# pip install "autogen-ext[openai, ollama]"

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
```

### gemini_client.py

```python
# gemini_client.py
# pip install pyautogen
# pip install google-genai
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
# pip install ddgs
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

if __name__ == "__main__": # only execute if the program is run directly and not loaded as a module via import
    print("🔍 Teste Web-Suche mit DuckDuckGo...\n")
    
    # Query-example
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
# openai_client.py    !This is a demo for a paid model!
# Register on https://platform.openai.com/ and obtain a free api-key (or pay if you like).
# Set an environment variable named "OPENAI_API_KEY" to the value of your API key.
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

## optionale Tests

- `demos/ollama_client.py` – Testet das lokal laufende Meta-LLM.  
   <small>Ausgabe: Ich bin Gemma, ein großes Sprachmodell, das von Google DeepMind trainiert wurde.
   Ich bin ein Open-Weights-Modell, das öffentlich verfügbar ist.
   Ich kann Text und Bilder als Eingabe nehmen und nur Text ausgeben.</small>
- `demos/gemini_client.py` – Testet das online laufende Google-LLM.
   <small>Ausgabe: AI lets computers learn from data to recognize patterns and make decisions.</small>
- `demos/duckduckgo_client.py` – Testet die Websuche über DuckDuckGo.
   <small>Ausgabe:  
     ...  
        "title": "Einwohnerbestand Berlin - Grunddaten",  
        "href": "https://www.statistik-berlin-brandenburg.de/a-i-5-hj",  
        "body": "Berliner Einwohnerbestand wächst weiter. Berlin zählte am 30. Juni 2025 insgesamt 3.902.645 Einwohnerinnen und Einwohner und verzeichnet gegenüber dem Vorjahr einen Zuwachs von 5.500 Personen. Die Zahl an Ausländerinnen und Ausländern war um 836 Personen auf 971.042 gesunken."  
   ...</small>
- Ggf. `demos/openai_client.py` – Testet das online laufende OpenAI-LLM.
   <small>Ausgabe: Exception has occurred: RateLimitError  
   Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details.  
   ...  
   Der Fehler ist plausibel, da das Modell aktuell kostenpflichtig ist
   und ich nichts bezahlen möchte.</small>

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
