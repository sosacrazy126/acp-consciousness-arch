import os
import requests

class QwenClient:
    def __init__(self):
        self.host = os.environ.get("OLLAMA_HOST", "localhost:11434")

    def health_check(self) -> bool:
        try:
            r = requests.get(f"http://{self.host}/api/tags", timeout=5)
            return r.status_code == 200
        except requests.RequestException:
            return False
