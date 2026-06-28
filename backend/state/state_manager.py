from enum import Enum
from datetime import datetime
from pathlib import Path
import json


class JarvisState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    RECORDING = "recording"
    TRANSCRIBING = "transcribing"
    THINKING = "thinking"
    SPEAKING = "speaking"
    ERROR = "error"
    SLEEPING = "sleeping"


class StateManager:
    def __init__(self, state_file="frontend/state.json"):
        self.state = JarvisState.IDLE
        self.last_updated = datetime.now()
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._write_state()

    def set_state(self, state: JarvisState):
        self.state = state
        self.last_updated = datetime.now()
        self._write_state()
        print(f"[STATE] {self.state.value.upper()}")

    def get_state(self):
        return {
            "state": self.state.value,
            "last_updated": self.last_updated.isoformat(),
        }

    def _write_state(self):
        self.state_file.write_text(
            json.dumps(self.get_state(), indent=2),
            encoding="utf-8",
        )
