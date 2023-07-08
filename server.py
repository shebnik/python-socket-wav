import wave
import socket
import threading

# Configure the initial buffer size and sample rate
BUFFER_SIZE = 128
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
    channels = audio_file.getnchannels()
    sample_width = audio_file.getsampwidth()

    # Send the initial buffer size, sample rate, and channels to the client
    params = f':{BUFFER_SIZE}:{SAMPLE_RATE}:{channels}:'.encode()
    conn.send(params)

    # Function to handle user input
    def handle_user_input():
        global BUFFER_SIZE, SAMPLE_RATE
        while True:
            command = input('Enter command (buffer, rate): ')
            if command == 'buffer':
                BUFFER_SIZE = int(input('Enter new buffer size: '))
                print('Buffer size updated.')
                # Send control message to client
                control_message = f'settings:{BUFFER_SIZE}:{SAMPLE_RATE}:{channels}:settings'.encode()
                conn.send(control_message)
            elif command == 'rate':
                SAMPLE_RATE = int(input('Enter new sample rate: '))
                print('Sample rate updated.')
                # Send control message to client
                control_message = f'settings:{BUFFER_SIZE}:{SAMPLE_RATE}:{channels}:settings'.encode()
                conn.send(control_message)
            else:
                print('Invalid command.')

    # Start a thread to handle user input
    user_input_thread = threading.Thread(target=handle_user_input)
    user_input_thread.daemon = True
    user_input_thread.start()

    # Read and stream the audio data
    data = audio_file.readframes(BUFFER_SIZE)
    while data:
        conn.send(data)
        data = audio_file.readframes(BUFFER_SIZE)

# Close the connection
conn.close()
sock.close()
