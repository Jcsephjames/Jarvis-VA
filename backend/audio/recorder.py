import wave
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

    def record(self, filename="recording.wav", duration=5):
        print(f"Recording for {duration} seconds...")

        stream = self.audio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        frames = []

        for _ in range(
            int(self.sample_rate / self.chunk_size * duration)
        ):
            data = stream.read(
                self.chunk_size,
                exception_on_overflow=False,
            )
            frames.append(data)

        stream.stop_stream()
        stream.close()

        with wave.open(filename, "wb") as wav:
            wav.setnchannels(self.channels)
            wav.setsampwidth(
                self.audio.get_sample_size(self.sample_format)
            )
            wav.setframerate(self.sample_rate)
            wav.writeframes(b"".join(frames))

        print(f"Saved recording to {filename}")

    def close(self):
        self.audio.terminate()
