import time
import wave

import pyaudio

from backend.vad.webrtc_vad import WebRTCVAD


class AudioRecorder:
    def __init__(
        self,
        sample_rate=16000,
        channels=1,
        chunk_size=480,
        sample_format=pyaudio.paInt16,
        vad=None,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.sample_format = sample_format
        self.vad = vad or WebRTCVAD(sample_rate=sample_rate)

        self.audio = pyaudio.PyAudio()

    def record_until_silence(
        self,
        filename="command.wav",
        silence_seconds=1.2,
        max_seconds=20,
        max_wait_for_speech_seconds=8,
    ):
        print("Waiting for speech...")

        stream = self.audio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        frames = []
        started_at = time.time()
        speech_started = False
        last_voice_time = None

        try:
            while True:
                data = stream.read(
                    self.chunk_size,
                    exception_on_overflow=False,
                )

                now = time.time()
                is_speech = self.vad.is_speech(data)

                if is_speech:
                    if not speech_started:
                        print("Speech detected. Recording...")

                    speech_started = True
                    last_voice_time = now
                    frames.append(data)

                elif speech_started:
                    frames.append(data)

                if not speech_started:
                    if now - started_at > max_wait_for_speech_seconds:
                        print("No speech detected. Cancelling recording.")
                        break
                    continue

                silence_duration = now - last_voice_time
                recording_duration = now - started_at

                if silence_duration > silence_seconds:
                    print("Silence detected. Stopping recording.")
                    break

                if recording_duration > max_seconds:
                    print("Max recording time reached. Stopping recording.")
                    break

        finally:
            stream.stop_stream()
            stream.close()

        if frames:
            self._save_wav(filename, frames)
            print(f"Saved recording to {filename}")
        else:
            print("No audio saved.")

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
