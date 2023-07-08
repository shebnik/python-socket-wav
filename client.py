import wave
import socket
import pyaudio
import re
import threading
import struct

# Create a socket and connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8000))

HEADER_FORMAT = "!IIII"  # Four unsigned integers, 8 bytes (64 bits)

# Receive the header data
header_data = sock.recv(16)

# Unpack the header
buffer_size, sample_rate, channels, sample_width = struct.unpack(HEADER_FORMAT, header_data)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a new audio stream
stream = p.open(
    format=p.get_format_from_width(sample_width),
    channels=channels,
    rate=sample_rate,
    output=True
)
print(f'Stream started with buffer size: {buffer_size}, sample rate: {sample_rate}, channels: {channels}, sample width: {sample_width}')
# Receive and play the audio data
data = sock.recv(buffer_size)
while data:
    # if 
    #     print('Received settings update.')
    #     buffer_size =
    #     sample_rate =
    #     channels =
    #     sample_width =
    #
    #     # Update the audio stream parameters
    #     stream.stop_stream()
    #     stream.close()
    #     stream = p.open(
    #         format=p.get_format_from_width(sample_width),
    #         channels=channels,
    #         rate=sample_rate,
    #         output=True
    #     )
    #     print(f'Updated to buffer size: {buffer_size}, sample rate: {sample_rate}, channels: {channels}, sample width: {sample_width}')
        
    stream.write(data)
    data = sock.recv(buffer_size)

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
sock.close()
