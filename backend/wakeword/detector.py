import time

import numpy as np
import pyaudio
from openwakeword.model import Model


class WakeWordDetector:
    def __init__(
        self,
        threshold=0.75,
        cooldown_seconds=8,
        sample_rate=16000,
        chunk_size=1280,
    ):
        self.threshold = threshold
        self.cooldown_seconds = cooldown_seconds
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.last_detection_time = 0

        self.model = Model()
        self.audio = pyaudio.PyAudio()
        self.stream = None

        self.open_stream()

    def open_stream(self):
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        self.flush_audio_chunks(10)

    def close_stream(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def flush_audio_chunks(self, chunks=10):
        if self.stream is None:
            return

        for _ in range(chunks):
            self.stream.read(
                self.chunk_size,
                exception_on_overflow=False,
            )

    def wait_for_wake_word(self):
        print("Listening for wake word...")

        while True:
            audio_data = self.stream.read(
                self.chunk_size,
                exception_on_overflow=False,
            )

            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            predictions = self.model.predict(audio_array)

            score = predictions.get("hey_jarvis", 0)

            if self._is_detection(score):
                self.last_detection_time = time.time()
                return "hey_jarvis", score

    def _is_detection(self, score):
        return (
            score > self.threshold
            and time.time() - self.last_detection_time > self.cooldown_seconds
        )

    def reset(self):
        self.close_stream()

        self.model.reset()
        self.last_detection_time = time.time()

        time.sleep(1.5)
        self.open_stream()

    def close(self):
        self.close_stream()
        self.audio.terminate()
