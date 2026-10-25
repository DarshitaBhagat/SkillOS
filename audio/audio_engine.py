import sounddevice as sd
import numpy as np
import librosa
import math
from collections import deque
import threading


class AudioEngine:

    def __init__(self, silence_threshold=0.008, buffer_size=2048):
        self.lock = threading.Lock()

        # audio settings
        self.samplerate = 22050
        self.blocksize = 1024
        self.buffer_size = buffer_size
        self.silence_threshold = silence_threshold

        # rolling buffer for pitch detection
        self.buffer = np.zeros(self.buffer_size, dtype=np.float32)

        # stabilization buffer (median smoothing over recent pitch readings)
        self.pitch_buffer = deque(maxlen=3)

        # latest detected note
        self.current_note = None

        self.stream = None

    def freq_to_note(self, freq):
        if freq is None or freq <= 0 or np.isnan(freq):
            return None

        midi = round(12 * math.log2(freq / 440.0) + 69)
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        note = notes[midi % 12]
        octave = midi // 12 - 1

        return f"{note}{octave}"

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"Audio stream status: {status}")

        audio = indata[:, 0]
        rms = np.sqrt(np.mean(audio**2))

        with self.lock:
            if rms < self.silence_threshold:
                # Signal is silent: roll in zeros and clear smoothed pitch history
                self.buffer = np.roll(self.buffer, -len(audio))
                self.buffer[-len(audio):] = 0.0
                self.pitch_buffer.clear()
                self.current_note = None
            else:
                self.buffer = np.roll(self.buffer, -len(audio))
                self.buffer[-len(audio):] = audio

    def process_pitch(self):
        with self.lock:
            buffer_copy = self.buffer.copy()

        # Silence check: never run YIN on silent or near-zero buffers
        rms = np.sqrt(np.mean(buffer_copy**2))
        if rms < self.silence_threshold:
            self.current_note = None
            return None

        # YIN pitch detection optimized for sub-10ms execution
        # fmin=65Hz accommodates guitar low E2 (82.4Hz) and Drop D (73.4Hz)
        frame_len = min(1024, len(buffer_copy))
        try:
            f0 = librosa.yin(
                buffer_copy,
                fmin=65,
                fmax=1000,
                sr=self.samplerate,
                frame_length=frame_len,
                hop_length=512
            )
        except Exception:
            self.current_note = None
            return None

        # Filter out boundary anomalies where YIN hits fmax or drops below fmin
        valid_f0 = f0[(f0 >= 65) & (f0 < 980) & (~np.isnan(f0))]
        if len(valid_f0) == 0:
            self.current_note = None
            return None

        raw_freq = float(np.median(valid_f0))
        if raw_freq <= 0:
            self.current_note = None
            return None

        # Median stabilization prevents phantom intermediate notes on transitions
        self.pitch_buffer.append(raw_freq)
        stable_freq = float(np.median(self.pitch_buffer))

        note = self.freq_to_note(stable_freq)
        self.current_note = note
        return note

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
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
            self.stream = None

    def get_detected_note(self):
        return self.current_note
