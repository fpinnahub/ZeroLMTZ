from typing import Optional
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# spaCy is used for English lemmatization
try:
    import spacy
    from spacy.cli import download as spacy_download
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "spaCy is required. Install dependencies in requirements.txt first."
    ) from e


class LemmatizeIn(BaseModel):
    text: str = Field(..., description="Input text to lemmatize")


class LemmatizeOut(BaseModel):
    lemmatized: str = Field(..., description="Lemmatized text")


app = FastAPI(title="Lemmatizer API", version="1.0.0")

_nlp = None  # will be initialized during lifespan
_model_name = "en_core_web_sm"


def _load_en_model(model_name: str = "en_core_web_sm"):
    global _nlp, _model_name
    _model_name = model_name
    try:
        _nlp = spacy.load(model_name)
    except Exception:
        # Try to download the model automatically, then load again.
        # If network is restricted, this will fail and we provide a clear message.
        try:
            spacy_download(model_name)
            _nlp = spacy.load(model_name)
        except Exception as e:  # pragma: no cover
            raise RuntimeError(
                f"spaCy model '{model_name}' is not installed. "
                f"Install it with: python -m spacy download {model_name}"
            ) from e

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the spaCy English model during app lifespan."""
    model_name = os.getenv("SPACY_MODEL", _model_name)
    _load_en_model(model_name)
    yield
    # No explicit cleanup required for spaCy model

# Attach lifespan to the app
app.router.lifespan_context = lifespan


@app.get("/healthz")
def healthz():
    return {"status": "ok", "model": _model_name, "loaded": _nlp is not None}


@app.post("/lemmatize", response_model=LemmatizeOut)
def lemmatize(payload: LemmatizeIn):
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="'text' must be a non-empty string")

    if _nlp is None:
        raise HTTPException(status_code=500, detail="spaCy model not loaded")

    doc = _nlp(payload.text)

    # Build the lemmatized text while preserving original whitespace.
    parts = []
    for token in doc:
        if token.is_alpha:
            lemma = token.lemma_
            # Handle older models that produce '-PRON-' for pronouns
            if lemma.lower() == "-pron-":
                lemma = token.lower_
            else:
                lemma = lemma.lower()
            parts.append(lemma + token.whitespace_)
        else:
            parts.append(token.text_with_ws)

    result = "".join(parts).strip()
    return LemmatizeOut(lemmatized=result)


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
