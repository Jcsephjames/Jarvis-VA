import requests


class OllamaClient:
    def __init__(
        self,
        base_url="http://192.168.0.178:11434",
        model="qwen2.5:3b",
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def chat(self, message):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are JARVIS, a concise, calm, British AI assistant. "
                            "Keep replies short and practical."
                        ),
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
