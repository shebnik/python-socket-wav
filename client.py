import wave
import socket
import pyaudio
import re
import threading

# Create a socket and connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8000))

# Receive the initial buffer size, sample rate, and channels from the server
params = sock.recv(1024).decode()
if params.startswith('settings:'):
    settings = params.split(':')
    buffer_size = int(settings[1])
    sample_rate = int(settings[2])
    channels = int(settings[3])
else:
    # Handle error or default values
    buffer_size = 1024
    sample_rate = 44100
    channels = 1

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a new audio stream
stream = p.open(
    format=p.get_format_from_width(2),
    channels=channels,
    rate=sample_rate,
    output=True
)
print(f'Stream started with buffer size: {buffer_size}, sample rate: {sample_rate}, channels: {channels}')
# Receive and play the audio data
data = sock.recv(buffer_size)
while data:
    if (b'settings:') in data:
        print('Received settings update.')
        encoded_settings = data[data.index(b'settings:'):data.index(b':settings')]
        settings = encoded_settings.decode().split(':')
        buffer_size = int(settings[1])
        sample_rate = int(settings[2])
        channels = int(settings[3])
        # Update the audio stream parameters
        stream.stop_stream()
        stream.close()
        stream = p.open(
            format=p.get_format_from_width(2),
            channels=channels,
            rate=sample_rate,
            output=True
        )
        print(f'Updated to buffer size: {buffer_size}, sample rate: {sample_rate}, channels: {channels}')
        
        # remove settings from data
        data = data.replace(encoded_settings, b'')
        
    stream.write(data)
    data = sock.recv(buffer_size)

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
sock.close()
