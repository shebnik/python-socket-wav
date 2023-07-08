import wave
import socket
import threading
import struct

# Configure the initial buffer size
buffer_size = 128
sample_rate = 44100

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.listen(1)
print('Listening on port 8000...')

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
    
    # data = audio_file.readframes(buffer_size)
    # header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width) 
    # conn.sendall(header_data+data)
    # print(f'data sent with size: {len(header_data+data)}')
    
    # data = audio_file.readframes(buffer_size)
    # buffer_size = 256
    # header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width)
    # conn.sendall(header_data+data)
    # print(f'data sent with size: {len(header_data+data)}')
    
    # data = audio_file.readframes(buffer_size)
    # header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width) 
    # conn.sendall(header_data+data)
    # print(f'data sent with size: {len(header_data+data)}')
    
    # data = audio_file.readframes(buffer_size)
    # buffer_size = 21
    # header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width)
    # conn.sendall(header_data+data)
    # print(f'data sent with size: {len(header_data+data)}')
    
    # data = audio_file.readframes(buffer_size)
    # header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width) 
    # conn.sendall(header_data+data)
    # print(f'data sent with size: {len(header_data+data)}')

    # Function to handle user input of buffer size or sample rate
    def handle_user_input():
        global buffer_size, sample_rate, header_data
        while True:
            option = input("buffer/rate: ")
            if option == "buffer":
                new_buffer_size = input("Enter the new buffer size: ")
                if new_buffer_size.isdigit():
                    # buffer_size = int(new_buffer_size)
                    header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width)
                    print("Buffer size updated to", buffer_size)
                else:
                    print("Invalid input. Buffer size unchanged.")
            elif option == "rate":
                new_sample_rate = input("Enter the new sample rate: ")
                if new_sample_rate.isdigit():
                    sample_rate = int(new_sample_rate)
                    header_data = struct.pack(HEADER_FORMAT, buffer_size, sample_rate, channels, sample_width)
                    print("Sample rate updated to", sample_rate)
                else:
                    print("Invalid input. Sample rate unchanged.")

    # Start a separate thread to handle user input
    thread = threading.Thread(target=handle_user_input)
    thread.start()

    # Read and stream the audio data
    data = audio_file.readframes(buffer_size)
    while data:
        # TODO: send header data with new buffer size + audio data with old buffer size
        # Possible TODO: reduce latency in settings change
        conn.sendall(header_data+data)          
        data = audio_file.readframes(buffer_size)

# Close the connection
conn.close()
sock.close()
