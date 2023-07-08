import wave
import socket
import pyaudio

# Create a socket and connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8000))

# Receive the buffer size, sample rate, and channels from the server
params = sock.recv(1024).decode()
buffer_size, sample_rate, channels = map(int, params.split(':'))

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a new audio stream
stream = p.open(
    format=p.get_format_from_width(2),
    channels=channels,  # Update channels parameter
    rate=sample_rate,
    output=True
)

# Receive and play the audio data
data = sock.recv(buffer_size)
while data:
    stream.write(data)
    data = sock.recv(buffer_size)

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
sock.close()
