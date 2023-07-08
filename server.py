import wave
import socket
import threading
import struct

# Configure the initial buffer size
BUFFER_SIZE = 256

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.listen(1)
print('Listening on port 8000...')

# Define the header structure
HEADER_FORMAT = "!IIII"

# Accept a client connection
conn, addr = sock.accept()
print('Connected by', addr)

# Open the wave file
with wave.open('audio.wav', 'rb') as audio_file:
    # Get the audio file parameters    
    sample_rate = audio_file.getframerate()
    channels = audio_file.getnchannels()
    sample_width = audio_file.getsampwidth()
    
    # Send the header data to the client
    header_data = struct.pack(HEADER_FORMAT, BUFFER_SIZE, sample_rate, channels, sample_width)
    print('Sending initial header data:', header_data)
    conn.sendall(header_data)

    # Function to handle user input of buffer size or sample rate
    

    # Read and stream the audio data
    data = audio_file.readframes(BUFFER_SIZE)
    while data:
        conn.sendall(data)
        data = audio_file.readframes(BUFFER_SIZE)

# Close the connection
conn.close()
sock.close()
