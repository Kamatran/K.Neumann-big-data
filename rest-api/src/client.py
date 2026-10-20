"""Calls the model service from a second container.

Note the address: the service name from the compose file, not localhost.
Inside a container, localhost means this container.
"""
import json
import urllib.error
import urllib.request

BASE = "http://api:8000"


def get(path):
    with urllib.request.urlopen(BASE + path) as r:
        return r.status, json.load(r)


def post(path, body):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return r.status, json.load(r)

print("GET  /labels  ->", *get("/labels"))
print("GET  /health  ->", *get("/health"))
print("GET  /model   ->", *get("/model"))
print("POST /predict ->", *post("/predict", {"text": "Szybka dostawa, polecam"}))
print("POST /predict ->", *post("/predict", {"text": "Awaria po dwoch dniach, rozczarowanie"}))
# Asked twice on purpose: loaded_at does not move, requests_served does.
print("GET  /model   ->", *get("/model"))

# The same call through localhost - inside this container nothing listens there.
try:
    with urllib.request.urlopen("http://localhost:8000/health") as r:
        print("localhost     ->", r.status)
except urllib.error.URLError as e:
    print("localhost     ->", type(e.reason).__name__, "- nothing is listening here")
