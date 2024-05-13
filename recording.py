

import pyaudio
import wave

# Configuration
FORMAT = pyaudio.paInt16       # Audio format (16-bit PCM)
CHANNELS = 1                    # Number of audio channels (mono)
RATE = 44100                    # Sample rate (samples per second)
CHUNK = 1024                    # Number of frames per buffer
WAVE_OUTPUT_FILENAME = "output.wav"

def start_audio():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... (Press Ctrl+C to stop)")

    frames = []

    # Record audio indefinitely until interrupted
    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        print("Recording stopped by user.")

    # Stop and close stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded audio to WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as '{WAVE_OUTPUT_FILENAME}'")

