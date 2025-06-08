import os
import time
import requests
from pathlib import Path


def wait_for_ollama(host, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"http://{host}/api/tags")
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(5)
    return False


def ensure_model_loaded(host, model):
    r = requests.get(f"http://{host}/api/tags")
    if r.status_code == 200:
        models = [m.get("name") for m in r.json().get("models", [])]
        if model not in models:
            print(f"Pulling model {model}...")
            pr = requests.post(f"http://{host}/api/pull", json={"name": model})
            pr.raise_for_status()

    # test generate
    tr = requests.post(
        f"http://{host}/api/generate",
        json={"model": model, "prompt": "test", "stream": False},
    )
    tr.raise_for_status()


if __name__ == "__main__":
    host = os.environ.get("OLLAMA_HOST", "localhost:11434")
    model = os.environ.get("MODEL_NAME", "qwen:0.6b")

    print(f"Waiting for Ollama at {host}...")
    if not wait_for_ollama(host):
        raise SystemExit("Ollama service not available")

    print(f"Ensuring model {model} is loaded...")
    ensure_model_loaded(host, model)
    print("Model setup complete")
