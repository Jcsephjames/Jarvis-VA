from faster_whisper import WhisperModel


class WhisperTranscriber:
    def __init__(self, model_size="tiny.en", device="cpu", compute_type="int8"):
        print(f"Loading Whisper model: {model_size}")

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, audio_file):
        segments, info = self.model.transcribe(audio_file)

        text_parts = []

        for segment in segments:
            text_parts.append(segment.text.strip())

        return " ".join(text_parts).strip()
