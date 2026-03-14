import sounddevice as sd
import numpy as np

def audio_callback(indata, frames, time, status):
    if status:
        print(status)

    audio = indata[:, 0]

    rms = np.sqrt(np.mean(audio**2))
    peak = np.max(np.abs(audio))

    print(f"RMS: {rms:.4f} | Peak: {peak:.4f}")

print("Mic stream started")

with sd.InputStream(callback=audio_callback,
                    channels=1,
                    samplerate=44100,
                    blocksize=2048):
    input("Press Enter to stop\n")
