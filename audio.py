import sounddevice as sd
import numpy as np
import librosa
import math

samplerate = 44100

def freq_to_note(freq):
    if freq <= 0:
        return None

    midi = round(12 * math.log2(freq / 440.0) + 69)

    notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    note = notes[midi % 12]
    octave = midi // 12 - 1

    return f"{note}{octave}"

def audio_callback(indata, frames, time, status):

    audio = indata[:,0]

    f0 = librosa.yin(audio,
                     fmin=70,
                     fmax=500,
                     sr=samplerate)

    freq = np.mean(f0)

    note = freq_to_note(freq)

    print(f"Freq: {freq:.2f} Hz | Note: {note}")

with sd.InputStream(callback=audio_callback,
                    channels=1,
                    samplerate=samplerate,
                    blocksize=4096):

    input("Listening...\n")