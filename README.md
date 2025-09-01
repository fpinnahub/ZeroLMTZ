# Lemmatizer API (spaCy)

A minimal FastAPI service that exposes a POST endpoint to lemmatize English text using spaCy.

## Setup

1. Create a virtual environment and install dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate` (Windows: `./.venv/Scripts/activate`)
   - `pip install -r requirements.txt`

2. Install the English model (required):
   - `python -m spacy download en_core_web_sm`

   Note: The app will attempt to download this automatically on first run; if your network is restricted, run the command above manually.

## Run

- `uvicorn app.main:app --reload --port 8000`

The API will be available at `http://localhost:8000`. Open `http://localhost:8000/docs` for interactive Swagger UI.

## Usage

POST `http://localhost:8000/lemmatize`

Body (JSON):

```
{ "text": "The striped bats are hanging on their feet for best" }
```

Response (JSON):

```
{ "lemmatized": "the striped bat be hang on their foot for good" }
```

Notes:
- Output preserves original whitespace and punctuation while lemmatizing alphabetic tokens.
- Pronouns from older spaCy models that yield `-PRON-` are handled gracefully.

## Health Check

- `GET /healthz` returns model load status.
