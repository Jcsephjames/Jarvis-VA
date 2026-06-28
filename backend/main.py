import subprocess

from backend.audio.recorder import AudioRecorder
from backend.brain.client import BrainClient
from backend.state.state_manager import JarvisState, StateManager
from backend.stt.whisper_transcriber import WhisperTranscriber
from backend.wakeword.detector import WakeWordDetector


def play_audio(filename):
    subprocess.run(["aplay", str(filename)], check=True)


def main():
    state = StateManager()

    detector = WakeWordDetector()
    recorder = AudioRecorder()
    transcriber = WhisperTranscriber()
    brain = BrainClient()

    print("JARVIS is online.")
    state.set_state(JarvisState.IDLE)

    try:
        while True:
            state.clear_interaction()
            state.set_state(JarvisState.LISTENING)
            wakeword, score = detector.wait_for_wake_word()

            print(f"Wake word detected: {wakeword} ({score:.2f})")
            detector.close_stream()

            state.set_state(JarvisState.RECORDING)
            recorder.record_until_silence(
                filename="command.wav",
                silence_seconds=1.2,
                max_seconds=20,
            )

            state.set_state(JarvisState.TRANSCRIBING)
            text = transcriber.transcribe("command.wav")
            print(f"You said: {text}")
            state.set_transcript(text)

            if not text:
                print("No speech detected. Resetting listener...")
                detector.reset()
                state.set_state(JarvisState.IDLE)
                continue

            state.set_state(JarvisState.THINKING)
            reply = brain.chat(text)
            print(f"JARVIS: {reply}")
            state.set_response(reply)

            state.set_state(JarvisState.SPEAKING)
            audio_file = brain.speak(reply)
            play_audio(audio_file)

            print("Resetting listener...")
            detector.reset()
            state.set_state(JarvisState.IDLE)

    except KeyboardInterrupt:
        print("\nShutting down JARVIS...")
        state.set_state(JarvisState.SLEEPING)

    except Exception as error:
        state.set_error(str(error))
        print(f"JARVIS error: {error}")
        raise

    finally:
        detector.close()
        recorder.close()


if __name__ == "__main__":
    main()
