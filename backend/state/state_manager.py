from enum import Enum
from datetime import datetime


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
    def __init__(self):
        self.state = JarvisState.IDLE
        self.last_updated = datetime.now()

    def set_state(self, state: JarvisState):
        self.state = state
        self.last_updated = datetime.now()
        print(f"[STATE] {self.state.value.upper()}")

    def get_state(self):
        return {
            "state": self.state.value,
            "last_updated": self.last_updated.isoformat(),
        }
