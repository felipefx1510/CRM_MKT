import logging

import requests


class OllamaService:
    def __init__(self, base_url, model, timeout=30):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def generate_summary(self, prompt):
        return self._generate(prompt)

    def generate_followup(self, prompt):
        return self._generate(prompt)

    def _generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "top_p": 0.9,
            },
        }
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except requests.RequestException:
            self.logger.exception("Ollama request failed")
            return ""
