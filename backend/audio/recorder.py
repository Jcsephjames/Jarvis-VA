import time
import wave

import numpy as np
import pyaudio


class AudioRecorder:
    def __init__(
        self,
        sample_rate=16000,
        channels=1,
        chunk_size=1024,
        sample_format=pyaudio.paInt16,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.sample_format = sample_format
        self.audio = pyaudio.PyAudio()

    def record_until_silence(
        self,
        filename="command.wav",
        silence_threshold=500,
        silence_seconds=1.2,
        max_seconds=20,
        min_seconds=1,
    ):
        print("Recording until you stop talking...")

        stream = self.audio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        frames = []
        started_at = time.time()
        last_voice_time = time.time()

        try:
            while True:
                data = stream.read(
                    self.chunk_size,
                    exception_on_overflow=False,
                )

                frames.append(data)

                audio_array = np.frombuffer(data, dtype=np.int16)
                volume = np.sqrt(np.mean(audio_array.astype(np.float32) ** 2))

                now = time.time()
                recording_duration = now - started_at
                silence_duration = now - last_voice_time

                if volume > silence_threshold:
                    last_voice_time = now

                if (
                    recording_duration > min_seconds
                    and silence_duration > silence_seconds
                ):
                    print("Silence detected. Stopping recording.")
                    break

                if recording_duration > max_seconds:
                    print("Max recording time reached. Stopping recording.")
                    break

        finally:
            stream.stop_stream()
            stream.close()

        self._save_wav(filename, frames)

        print(f"Saved recording to {filename}")

    def _save_wav(self, filename, frames):
        with wave.open(filename, "wb") as wav:
            wav.setnchannels(self.channels)
            wav.setsampwidth(
                self.audio.get_sample_size(self.sample_format)
            )
            wav.setframerate(self.sample_rate)
            wav.writeframes(b"".join(frames))

    def close(self):
        self.audio.terminate()
