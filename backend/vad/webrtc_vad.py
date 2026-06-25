import webrtcvad


class WebRTCVAD:
    def __init__(self, aggressiveness=2, sample_rate=16000):
        self.vad = webrtcvad.Vad(aggressiveness)
        self.sample_rate = sample_rate

    def is_speech(self, audio_chunk):
        return self.vad.is_speech(audio_chunk, self.sample_rate)
