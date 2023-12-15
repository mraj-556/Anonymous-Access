import pyaudio
import socket

# Set parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize PyAudio object
audio = pyaudio.PyAudio()

# Open the microphone stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

# Set up socket connection
host = 'localhost'
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Send audio data over socket
while True:
    data = stream.read(CHUNK)
    s.sendall(data)

# Stop and close the microphone stream
stream.stop_stream()
stream.close()
audio.terminate()

# Close the socket connection
s.close()
