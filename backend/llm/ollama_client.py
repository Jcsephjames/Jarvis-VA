from pathlib import Path

import requests


class OllamaClient:
    def __init__(
        self,
        base_url="http://192.168.0.178:11434",
        model="qwen2.5:3b",
        system_prompt_path="backend/prompts/jarvis_identity.md",
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.system_prompt = Path(system_prompt_path).read_text().strip()

    def chat(self, message):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": message,
                    },
                ],
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

        return data["message"]["content"].strip()
