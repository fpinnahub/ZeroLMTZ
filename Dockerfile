# syntax=docker/dockerfile:1

ARG PYTHON_IMAGE=python:3.11-slim
FROM ${PYTHON_IMAGE} AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    SPACY_MODEL=en_core_web_sm

WORKDIR /app

# Install system deps only if needed. spaCy and numpy wheels are prebuilt for linux/amd64.
# If you hit build issues on other platforms, consider adding build tools:
#   run apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better layer caching
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Download the spaCy model at build time so runtime is fully offline
RUN python -m spacy download ${SPACY_MODEL}

# Copy app code
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

