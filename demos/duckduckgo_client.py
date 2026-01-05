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
    