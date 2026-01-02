------------------------------------------------------------------------------------------
d:\Daten\private4\AI\Agent_System\ReadMe!.txt
Stand: 01.01.2026
------------------------------------------------------------------------------------------
Ollama KI-Client (grafisches Tool mit Tray-Symbol)

	https://ollama.com/download
	Herunterladen und installieren.

	Eine neue Umgebungsvariable mit dem Namen OLLAMA_MODELS erstellen
	und als Wert den Pfad zum gewünschten Speicherort der Modelle angeben.

	Ggf. Modelle für den lokalen Betrieb herunterladen.
	Geht direkt über den Ollama KI-Client oder über beispielsweise
	ollama pull deepseek-r1:7b (oder ollama pull deepseek-r1 (entspricht 7B), 1.5B, 7B, 14B und 70B)
	Dieser Befehl lädt das DeepSeek-R1 Modell herunter.
	Je nach Internetgeschwindigkeit kann dies einige Zeit in Anspruch nehmen.

	Installation überprüfen:
	ollama list
	ollama ps (zeigt die Modelle, auf die kürzlich zugegriffen wurde)

	Für Kommandozeilen-Tests (nicht nötig für die Python-KI-Zugriffe):
	ollama run deepseek-r1

Python KI-Zugriffe

	Neuen Ordner anlegen, z.B.: "Agent_System" und mit vscode öffnen.
	Unterodner "config", "tools", "agents" anlegen.
	
	python -m venv myvenv/
	Bei Fehlern einfach wiederholen, bis es klappt (Timing Problem bei pip)
	
	./myvenv/Scripts/activate.ps1
	
	Strg-Umschalt-p und Python: Select Interpreter, 
	dort myvenv (3.14.2) .\myvenv\Scripts\python.exe Recommended
	
	für den Debugger: Run/Add Configuration
	...
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
	...
	
	python -m pip install --upgrade pip
	pip install pyautogen

	pip install openai
	agents/check_ollama.py debuggen (testet das lokal laufende Meta-LLM gemma3:4b)
		Ergebnis:
		Ich bin Gemma, ein großes Sprachmodell, das von Google DeepMind trainiert wurde.
		Ich bin ein Open-Weights-Modell, das der Öffentlichkeit frei zugänglich ist.
		Ich bin darauf trainiert, Text und Bilder zu verstehen und daraufhin Text auszugeben.
		Du kannst mich gerne fragen!
	
	pip install google-genai
	tools/gemini_client debuggen (testet das online laufende Google-LLM gemini-2.5-flash)
		Ergebnis:
		AI learns patterns from data to make smart decisions or predictions.
	
	pip install ddgs
	tools/duckduckgo_client.py debuggen (testet die Websuche über duckduckgo (ddgs))

Wenn alles fehlerfrei funktioniert, dann noch:
pip freeze > requirements.txt

------------------------------------------------------------------------------------------
Ggf. noch:
tools/autogen_client.py debuggen (testet das online laufende OpenAI-Modell gpt-4o)
Error code: 429 - {'error': {'message': 'You exceeded your current quota,
please check your plan and billing details...
Dieser Fehler ist plausibel, da das Modell zur Zeit kostenpflichtig ist
(und ich nichts bezahlen will).

------------------------------------------------------------------------------------------
Sourcecode des funktionierenden Scrips "llm_config.py":
------------------------------------------------------------------------------------------
# llm_config.py
LLM_CONFIG_OLLAMA: dict[str, list[dict[str, str]] | float] = {
    "config_list": [
        {
            # "model": "gemma3:4b",
            "model": "deepseek-r1:7b",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",  # Pflichtfeld, wird ignoriert
        }
    ],
    "temperature": 0.7,
}
------------------------------------------------------------------------------------------
Sourcecode des funktionierenden Scrips "check_ollama.py":
------------------------------------------------------------------------------------------
# check_ollama.py
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
------------------------------------------------------------------------------------------
Sourcecode des funktionierenden Scrips "duckduckgo_client.py":
------------------------------------------------------------------------------------------
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

###########
# M A I N #
###########

if __name__ == "__main__": # nur ausführen, wenn das Programm direkt ausgeführt wird und nicht über import als Modul geladen wurde
    print("🔍 Teste Web-Suche mit DuckDuckGo...\n")
    
    # Beispiel-Suche
    test_query = "aktuelle Bevölkerung von Berlin 2025"
    print(f"Suche: '{test_query}'\n")
    
    result = search_web(test_query, max_results=2)
    print("Ergebnis:")
    print(result)
    print("\n✅ Test abgeschlossen.")

------------------------------------------------------------------------------------------
Tabelle der im Ollama-Client (Tray-Symbol) angezeigten Modelle
und ihrer Hardware-Anforderungen
------------------------------------------------------------------------------------------
Modell	Größe (Parameter)	Benötigter VRAM (ca.)	Hardware-Klasse
gpt-oss:120b	120 Mrd.	~70-80 GB	High-End Workstation (z.B. 4x RTX 4090)
qwen3-coder:30b	30 Mrd.	~20-24 GB	Enthusiast (z.B. RTX 3090 / 4090)
qwen3:30b	30 Mrd.	~20-24 GB	Enthusiast (z.B. RTX 3090 / 4090)
qwen3-vl:30b	30 Mrd.	~22-26 GB	Enthusiast (Grafikkarte mit viel VRAM)
gemma3:27b	27 Mrd.	~18-22 GB	Oberklasse (RTX 3090 / 4090)
gpt-oss:20b	20 Mrd.	~14-16 GB	Mittelklasse (RTX 3080 16GB / 4070 Ti Super)
gemma3:12b	12 Mrd.	~8-10 GB	Mittelklasse (RTX 3060 12GB / 4070)
deepseek-r1:8b	8 Mrd.	~6-8 GB	Standard PC (RTX 3060 / 4060)
qwen3-vl:8b	8 Mrd.	~6-8 GB	Standard PC
qwen3:8b	8 Mrd.	~6-8 GB	Standard PC
llama3:8b	8 Mrd.	~6-8 GB	Standard PC
deepseek-r1:7b	7 Mrd.	~5-6 GB	Einsteiger / Laptop
gemma3:4b	4 Mrd.	~3-4 GB	Einsteiger / Laptop
qwen3-vl:4b	4 Mrd.	~3-4 GB	Einsteiger / Laptop
qwen3:4b	4 Mrd.	~3-4 GB	Einsteiger / Laptop
gemma3:1b	1 Mrd.	~1-2 GB	Läuft fast überall