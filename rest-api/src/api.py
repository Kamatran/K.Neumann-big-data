"""A service that serves a model behind an HTTP contract.

The "model" here is deliberately a stub: a fixed word list with fixed weights.
Nothing is learned, and the result is fully deterministic. That is the point -
everything this week is about what surrounds a model (an image, a port, a
contract, a client), not about the model itself. Whatever sits behind /predict
could be a rule or a network with a billion weights; for every other container
it makes no difference as long as the contract holds.

Training and tracking real models is the subject of the Machine Learning course.
"""
import time

from fastapi import FastAPI
from pydantic import BaseModel

MODEL_NAME = "sentiment-pl"
MODEL_VERSION = "0.1"
LABELS = ["pozytywna", "negatywna", "neutralna"]

# The "weights". Loaded once, when the process starts - not per request.
WEIGHTS = {
    "dobry": 1, "dobra": 1, "swietny": 1, "swietna": 1, "polecam": 1,
    "szybki": 1, "szybka": 1, "tani": 1, "tania": 1, "zadowolony": 1,
    "zly": -1, "zla": -1, "okropny": -1, "okropna": -1, "wolny": -1,
    "wolna": -1, "drogi": -1, "droga": -1, "awaria": -1, "rozczarowanie": -1,
}

app = FastAPI(title="model-api")

STATE = {"loaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "requests_served": 0}


class Text(BaseModel):
    text: str


def tokenize(text):
    return [t.strip(".,!?;:()\"'").lower() for t in text.split() if t.strip(".,!?;:()\"'")]

@app.get("/labels")
def labels():
    return {"labels": LABELS}

@app.get("/health")
def health():
    """Used by the healthcheck in compose - it must stay cheap and side-effect free."""
    return {"status": "ok", "service": "model-api"}


@app.get("/model")
def model():
    """Metadata, not a prediction. Shows that the model was loaded once and that
    this container keeps state between calls."""
    return {
        "name": MODEL_NAME,
        "version": MODEL_VERSION,
        "loaded_at": STATE["loaded_at"],
        "requests_served": STATE["requests_served"],
        "vocabulary_size": len(WEIGHTS),
    }


@app.post("/predict")
def predict(payload: Text):
    tokens = tokenize(payload.text)
    if not tokens:
        return {"error": "empty text"}
    hits = sum(WEIGHTS.get(t, 0) for t in tokens)
    label = "neutralna" if hits == 0 else ("pozytywna" if hits > 0 else "negatywna")
    STATE["requests_served"] += 1
    return {
        "label": label,
        "score": round(abs(hits) / len(tokens), 3),
        "tokens": len(tokens),
        "model": f"{MODEL_NAME}-{MODEL_VERSION}",
    }

# TODO (zadanie Z7): dodaj punkt koncowy GET /labels zwracajacy liste mozliwych etykiet.
# Klient musi je znac, zanim wysle pierwsze zapytanie - to czesc kontraktu uslugi.
