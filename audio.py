import sounddevice as sd
import numpy as np
import librosa
import math
from collections import deque

samplerate = 44100

pitch_buffer = deque(maxlen=5)

def freq_to_note(freq):
    midi = round(12 * math.log2(freq / 440.0) + 69)
    notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    return notes[midi % 12]

def audio_callback(indata, frames, time, status):

    audio = indata[:,0]

    rms = np.sqrt(np.mean(audio**2))

    if rms < 0.01:
        return

    f0 = librosa.yin(audio,
                     fmin=80,
                     fmax=1000,
                     sr=samplerate)

    freq = np.mean(f0)

    pitch_buffer.append(freq)

    stable_freq = np.mean(pitch_buffer)

    note = freq_to_note(stable_freq)

    print(f"{stable_freq:.2f} Hz | {note}")

with sd.InputStream(callback=audio_callback,
                    channels=1,
                    samplerate=samplerate,
                    blocksize=4096):

    input("Listening...\n")
    