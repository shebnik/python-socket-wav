import wave
import socket
import pyaudio
import re
import threading
import struct
import time
from datetime import datetime

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
i = 0
data = sock.recv(buffer_size * 4 + 16)
while data:
    # # DEBUG
    # timestamp = time.time()
    # formatted_time = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S:%f')
    # print(str(formatted_time) + ' - ' + str(i))
    # with open('output.txt', 'a') as f:
    #     f.write(str(i)  + f': {buffer_size} - ' + str(data)+ '\n')
    
    # with open('header.txt', 'a') as f:
    #     f.write(str(data[:16]) + '\n')

    _buffer_size = buffer_size
    _sample_rate = sample_rate
    _channels = channels
    _sample_width = sample_width
    
    try:
        _buffer_size, _sample_rate, _channels, _sample_width = struct.unpack(HEADER_FORMAT, data[:16])
    except:
        print('Error unpacking header')
        print(str(i) + ': ' + str(data))        
        
    if _buffer_size != buffer_size:
        print(f'Buffer size changed from {buffer_size} to {_buffer_size}')
        buffer_size = _buffer_size
    if _sample_rate != sample_rate:
        print(f'Sample rate changed from {sample_rate} to {_sample_rate}')
        sample_rate = _sample_rate
        # Stop and close the current audio stream
        stream.stop_stream()
        stream.close()
        # Open a new audio stream with the updated sample rate
        stream = p.open(
            format=p.get_format_from_width(sample_width),
            channels=channels,
            rate=sample_rate,
            output=True
        )
    if _channels != channels:
        print(f'Channels changed from {channels} to {_channels}')
        channels = _channels
        # Stop and close the current audio stream
        stream.stop_stream()
        stream.close()
        # Open a new audio stream with the updated number of channels
        stream = p.open(
            format=p.get_format_from_width(sample_width),
            channels=channels,
            rate=sample_rate,
            output=True
        )
    if _sample_width != sample_width:
        print(f'Sample width changed from {sample_width} to {_sample_width}')
        sample_width = _sample_width
        # Stop and close the current audio stream
        stream.stop_stream()
        stream.close()
        # Open a new audio stream with the updated sample width
        stream = p.open(
            format=p.get_format_from_width(sample_width),
            channels=channels,
            rate=sample_rate,
            output=True
        )
    
    # Write the audio data to the stream
    data = data[16:]
    stream.write(data)
    
    # Send acknowledgment to the server
    sock.send(b'A')
    
    # Receive the next chunk of audio data
    data = sock.recv(buffer_size * 4 + 16)
    i += 1

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
sock.close()
