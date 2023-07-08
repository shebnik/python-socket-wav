import wave
import socket

# Configure the buffer size and sample rate
BUFFER_SIZE = 1024
SAMPLE_RATE = 44100

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.listen(1)
print('Listening on port 8000...')

# Accept a client connection
conn, addr = sock.accept()
print('Connected by', addr)

# Open the wave file
with wave.open('audio.wav', 'rb') as audio_file:
    # Get the audio file parameters
    channels = audio_file.getnchannels()  # Update channels variable

    # Send the buffer size, sample rate, and channels to the client
    params = f'{BUFFER_SIZE}:{SAMPLE_RATE}:{channels}'.encode()
    conn.send(params)

    # Read and stream the audio data
    data = audio_file.readframes(BUFFER_SIZE)
    while data:
        conn.send(data)
        data = audio_file.readframes(BUFFER_SIZE)

# Close the connection
conn.close()
sock.close()
