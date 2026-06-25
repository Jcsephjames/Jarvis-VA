import numpy as np


class VolumeVAD:
    def __init__(self, threshold=700):
        self.threshold = threshold

    def is_speech(self, audio_chunk):
        audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
        volume = np.sqrt(np.mean(audio_array.astype(np.float32) ** 2))

        return volume > self.threshold
