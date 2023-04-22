import pyaudio
import socket , wave

# Set parameters for audio playback
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize PyAudio object
audio = pyaudio.PyAudio()

# Set up socket connection
host = 'localhost'
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

# Open the audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    output=True, frames_per_buffer=CHUNK)

wf = wave.open("received_audio.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)

# Receive audio data from socket and play back audio
while True:
    data = conn.recv(CHUNK)
    if not data:
        break
    # stream.write(data)
    wf.writeframes(data)

# Stop and close the audio stream
stream.stop_stream()
stream.close()
audio.terminate()

# Close the socket connection
wf.close()
conn.close()
