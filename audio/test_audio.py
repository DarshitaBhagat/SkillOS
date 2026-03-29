import time
from audio_engine import AudioEngine

audio = AudioEngine()

audio.start()

print("Listening... Play your guitar")

try:

   while True:
    note = audio.process_pitch()
    if note:
        print("Detected:", note)

        time.sleep(0.1)

except KeyboardInterrupt:

    print("Stopping audio")

    audio.stop()
    