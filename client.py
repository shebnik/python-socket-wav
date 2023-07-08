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
data = sock.recv(buffer_size * 4 + 16)
while data:
    buffer_size, sample_rate, channels, sample_width = struct.unpack(HEADER_FORMAT, data[:16])
    # print(f'Buffer size: {buffer_size}, sample rate: {sample_rate}, channels: {channels}, sample width: {sample_width}')
    # print(f'received data with size: {len(data)}, next data to recieve size is: {buffer_size * 4 + 16}')
    # if _buffer_size != buffer_size or _sample_rate != sample_rate or _channels != channels or _sample_width != sample_width:
        # print(f'Buffer size: {_buffer_size}, sample rate: {_sample_rate}, channels: {_channels}, sample width: {_sample_width}')
    # if b'\\' in data:
    #     print(data[data.index(b'{'):data.index(b'}')+1])
    # if len(data) != buffer_size:
    #     print(len(data))
    # try:
    #     buffer_size, sample_rate, channels, sample_width = struct.unpack(HEADER_FORMAT, data)
    #     print('Received data:', data)
    # except:
    with open('output.txt', 'a') as f:
        f.write(f'Buffer size: {buffer_size}, sample rate: {sample_rate}, channels: {channels}, sample width: {sample_width}\n')
    data = data[16:]
    stream.write(data)
    data = sock.recv(buffer_size * 4 + 16)

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
sock.close()
