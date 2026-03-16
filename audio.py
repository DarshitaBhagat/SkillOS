import sounddevice as sd
import numpy as np
import librosa
import math
from collections import deque

samplerate = 44100

# rolling audio window
buffer = np.zeros(8192)

# smoothing buffer
pitch_buffer = deque(maxlen=5)


def freq_to_note(freq):

    midi = round(12 * math.log2(freq / 440.0) + 69)

    notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

    return notes[midi % 12]


def audio_callback(indata, frames, time, status):

    global buffer

    audio = indata[:,0]

    # silence filter
    rms = np.sqrt(np.mean(audio**2))
    if rms < 0.01:
        return

    # update rolling buffer
    buffer = np.roll(buffer, -len(audio))
    buffer[-len(audio):] = audio

    # pitch detection
    f0 = librosa.yin(buffer,
                     fmin=80,
                     fmax=1000,
                     sr=samplerate)

    freq = np.mean(f0)

    # stabilization
    pitch_buffer.append(freq)
    stable_freq = np.mean(pitch_buffer)

    note = freq_to_note(stable_freq)

    print(f"{stable_freq:.2f} Hz | {note}")


with sd.InputStream(callback=audio_callback,
                    channels=1,
                    samplerate=samplerate,
                    blocksize=512):

    input("Running pitch detection...\n")