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
{
  "lemmatized": "the striped bat be hang on their foot for good",
  "tokens": [
    {"text":"The","lemma":"the","pos":"DET","tag":"DT","morph":"Definite=Def|PronType=Art"},
    {"text":"striped","lemma":"striped","pos":"ADJ","tag":"JJ","morph":"Degree=Pos"},
    {"text":"bats","lemma":"bat","pos":"NOUN","tag":"NNS","morph":"Number=Plur"},
    {"text":"are","lemma":"be","pos":"AUX","tag":"VBP","morph":"Mood=Ind|Tense=Pres|VerbForm=Fin"},
    {"text":"hanging","lemma":"hang","pos":"VERB","tag":"VBG","morph":"Tense=Pres|VerbForm=Part"},
    {"text":"on","lemma":"on","pos":"ADP","tag":"IN","morph":""},
    {"text":"their","lemma":"they","pos":"PRON","tag":"PRP$","morph":"Case=Gen|Number=Plur|Person=3|Poss=Yes|PronType=Prs"},
    {"text":"feet","lemma":"foot","pos":"NOUN","tag":"NNS","morph":"Number=Plur"},
    {"text":"for","lemma":"for","pos":"ADP","tag":"IN","morph":""},
    {"text":"best","lemma":"good","pos":"ADJ","tag":"JJS","morph":"Degree=Sup"}
  ]
}
```

Notes:
- Output preserves original whitespace and punctuation while lemmatizing alphabetic tokens.
- Pronouns from older spaCy models that yield `-PRON-` are handled gracefully.

## Health Check

- `GET /healthz` returns model load status.

## Docker

You can build a self-contained image that already includes the spaCy model (no runtime download needed).

Build:
- `docker build -t lemmatizer:latest .`

Run:
- `docker run --rm -p 8009:8000 lemmatizer:latest`

Choose model at build or run time:
- Build with a different base model: `docker build --build-arg SPACY_MODEL=en_core_web_md -t lemmatizer:md .`
- Or override at runtime (model must have been downloaded at build):
  - `docker run -e SPACY_MODEL=en_core_web_sm -p 80098000 lemmatizer:latest`

Docker Compose:
- `docker compose up --build`
- Override model: `SPACY_MODEL=en_core_web_md docker compose up --build`

Notes:
- The Dockerfile downloads the spaCy model during build, so the container can run offline.
- If you encounter build issues on non-amd64 platforms, consider enabling build tools in the Dockerfile (see commented apt-get line).
