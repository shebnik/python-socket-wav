import wave
import socket
import threading
import struct
import time
from datetime import datetime

# Configure the initial buffer size
sample_rate = 44100
buffer_size = round(sample_rate * 0.01)  # 10 ms for 44.1 kHz sample rate
print(f'Initial buffer size: {buffer_size}')

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.listen(1)
print('Listening on port 8000...')

new_buffer_size = None
# Function to handle user input of buffer size or sample rate
def handle_user_input():
    global buffer_size, sample_rate, header_data, new_buffer_size
    while True:
        option = input("buffer/rate: ")
        if option == "buffer" or option == "b" or option == "1":
            value = input("Enter the new buffer size: ")
            if value.isdigit():
                new_buffer_size = int(value)
                header_data = struct.pack(HEADER_FORMAT, new_buffer_size, sample_rate, channels, sample_width)
                print("Buffer size updated to", buffer_size)
            else:
                print("Invalid input. Buffer size unchanged.")
        elif option == "rate" or option == "r" or option == "2":
            new_sample_rate = input("Enter the new sample rate: ")
            if new_sample_rate.isdigit():
                sample_rate = int(new_sample_rate)
                header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width)
                print("Sample rate updated to", sample_rate)
            else:
                print("Invalid input. Sample rate unchanged.")
                
# Start a separate thread to handle user input
thread = threading.Thread(target=handle_user_input)

# Accept a client connection
conn, addr = sock.accept()
print('Connected by', addr)

HEADER_FORMAT = "!IIII"

# Open the wave file
with wave.open('audio.wav', 'rb') as audio_file:
    # Get the audio file parameters    
    sample_rate = audio_file.getframerate()
    channels = audio_file.getnchannels()
    sample_width = audio_file.getsampwidth()
    
    # Send the header data to the client
    header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width)
    conn.sendall(header_data)
        
    # Start the thread to handle user settings input
    thread.start()
    
    # Read and stream the audio data
    i = 0
    data = audio_file.readframes(buffer_size)
    while data:        
        # timestamp = time.time()
        # formatted_time = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S:%f')
        # print(str(formatted_time) + ' - ' + str(i))
        
        conn.sendall(header_data + data)
        if new_buffer_size is not None:
            buffer_size = new_buffer_size
            new_buffer_size = None
        
        # Wait for acknowledgment from the client
        ack = conn.recv(1)
        
        # Check if acknowledgment is received
        if ack == b'A':
            data = audio_file.readframes(buffer_size)
            i += 1

# Close the connection
conn.close()
sock.close()
thread.stop()