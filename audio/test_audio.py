import time
from audio_engine import AudioEngine

audio = AudioEngine()

audio.start()

print("Listening... Play your guitar")

try:

    while True:

        note = audio.get_detected_note()

        if note:
            print("Detected:", note)

        time.sleep(0.1)

except KeyboardInterrupt:

    print("Stopping audio")

    audio.stop()
    