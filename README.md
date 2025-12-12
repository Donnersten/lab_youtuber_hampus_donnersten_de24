# lab_youtuber_hampus_donnersten_de24

Enkel RAG-prototyp som svarar på frågor om YouTube-transkript. Backend med LanceDB och Gemini, frontend är en Streamlit chat som anropar en Azure Function.

## Arkitektur i korthet
- `ingestion.py` skapar en LanceDB-tabell och laddar in transkript från `data/`.
- `api.py` exponerar endpointen `/rag/query` som använder `backend/rag.py` och Gemini-2.5-flash för att hämta svar baserat på närmaste transkript.
- `function_app.py` exponerar FastAPI-appen via Azure Functions.
- `frontend/app.py` är Streamlit-chatten som skickar frågor till Azure Function URL:en.

## Förutsättningar
- Python 3.10+ och `uv`.
- Azure Function-nyckel samt Gemini-API-nyckel.

## Installation
- `uv sync` om du använder uv och `uv.lock`.
- Lägg en `.env` i projektroten med:
  - `GOOGLE_API_KEY`
  - `FUNCTION_APP_API`.

## Köra lokalt
- Bygg vektorbasen från markdown-filer i `data/`: `python ingestion.py`.
- Starta API:t lokalt: `uvicorn api:app --reload`.
- Starta frontend-chatten: `streamlit run frontend/app.py`.

## Azure Function
- `function_app.py` använder `func.AsgiMiddleware` för att publicera FastAPI-appen som en HTTP-trigger.
- I Azure Portal: gå till din Function App -> Functions -> välj funktionen -> `Get Function URL` och kopiera nyckeln (`code`-parametern).
- Frontend anropar: `https://labb-youtuber.azurewebsites.net/rag/query?code={os.getenv('FUNCTION_APP_API')})` (se `frontend/app.py`). Ersätt hosten med den du får av Azure och lägg nyckeln i `.env` som `FUNCTION_APP_API`.

### Flöde
- Användaren skriver i Streamlit-chatten, som gör en POST mot Azure Function-URL:en.
- Azure Function skickar vidare till FastAPI (`api.py`), som kallar RAG-agenten.
- RAG-agenten plockar kontext från LanceDB och genererar svar med Gemini.
- Svar och källfil returneras till frontend och visas i chatten.

## Projektstruktur (kort)
```
.
├── backend/           RAG-agent datamodeller
├── data/              Transkript i markdown som laddas in i LanceDB
├── frontend/app.py    Streamlit-chat som anropar Azure Function
├── function_app.py    Azure Function till FastAPI
├── api.py             FastAPI-app med rag och query
├── ingestion.py       Bygger LanceDB-tabell från data
├── requirements.txt   Beroenden till Azure function
└── uv.lock / pyproject.toml  uv-lock och projektmetadata
```
