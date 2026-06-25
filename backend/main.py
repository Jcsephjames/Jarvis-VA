import time

from backend.audio.recorder import AudioRecorder
from backend.wakeword.detector import WakeWordDetector
from backend.stt.whisper_transcriber import WhisperTranscriber

def main():
    detector = WakeWordDetector()
    recorder = AudioRecorder()

    transcriber = WhisperTranscriber()

    print("JARVIS is online.")

    try:
        while True:
            wakeword, score = detector.wait_for_wake_word()

            print(f"Wake word detected: {wakeword} ({score:.2f})")
            print("Pausing wake word detector...")
            detector.close_stream()

            print("Recording command...")
            recorder.record_until_silence(
                filename="command.wav",
                silence_seconds=1.2,
                max_seconds=20,
            )
            text = transcriber.transcribe("command.wav")
            print(f"You said: {text}")

            print("Resetting listener...")
            detector.reset()

    except KeyboardInterrupt:
        print("\nShutting down JARVIS...")

    finally:
        detector.close()
        recorder.close()


if __name__ == "__main__":
    main()
