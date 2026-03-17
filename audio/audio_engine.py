import sounddevice as sd
import numpy as np
import librosa
import math
from collections import deque


class AudioEngine:

    def __init__(self):

        # audio settings
        self.samplerate = 44100
        self.blocksize = 512

        # rolling buffer for pitch detection
        self.buffer = np.zeros(8192)

        # stabilization buffer
        self.pitch_buffer = deque(maxlen=5)

        # latest detected note
        self.current_note = None

        self.stream = None


    def freq_to_note(self, freq):

        if freq <= 0:
            return None

        midi = round(12 * math.log2(freq / 440.0) + 69)

        notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

        note = notes[midi % 12]
        octave = midi // 12 - 1

        return f"{note}{octave}"


    def audio_callback(self, indata, frames, time, status):

        if status:
            print(status)

        audio = indata[:,0]

        # silence detection
        rms = np.sqrt(np.mean(audio**2))
        if rms < 0.01:
            return

        # update rolling buffer
        self.buffer = np.roll(self.buffer, -len(audio))
        self.buffer[-len(audio):] = audio

        # pitch detection
        f0 = librosa.yin(
            self.buffer,
            fmin=80,
            fmax=1000,
            sr=self.samplerate
        )

        freq = np.mean(f0)

        # stabilization smoothing
        self.pitch_buffer.append(freq)
        stable_freq = np.mean(self.pitch_buffer)

        # convert to note
        note = self.freq_to_note(stable_freq)

        # store result
        
        self.current_note = note


    def start(self):

        self.stream = sd.InputStream(
            callback=self.audio_callback,
            channels=1,
            samplerate=self.samplerate,
            blocksize=self.blocksize
        )

        self.stream.start()


    def stop(self):

        if self.stream:
            self.stream.stop()
            self.stream.close()


    def get_detected_note(self):
        return self.current_note