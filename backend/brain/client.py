from pathlib import Path

import requests


class BrainClient:
    def __init__(
        self,
        base_url="http://192.168.0.178:8000",
        output_audio_path="jarvis_response.wav",
    ):
        self.base_url = base_url.rstrip("/")
        self.output_audio_path = Path(output_audio_path)

    def chat(self, message: str) -> str:
        response = requests.post(
            f"{self.base_url}/chat",
            json={"message": message},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["reply"].strip()

    def speak(self, text: str) -> Path:
        response = requests.post(
            f"{self.base_url}/tts",
            json={"text": text},
            timeout=120,
        )
        response.raise_for_status()

        self.output_audio_path.write_bytes(response.content)
        return self.output_audio_path
