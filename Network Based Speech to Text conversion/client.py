import socket
import pyaudio

# HOST = '192.168.223.117'  # Server IP address
HOST = '192.168.53.115'  # Server IP address
PORT = 5000  # Arbitrary non-privileged port


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Unable to connect to the server. Make sure it is running and try again.")
    exit(1)


chunk_size = 1024
sample_rate = 44100
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

print('Recording...')

frames = []
for i in range(0, int(sample_rate / chunk_size * 5)):
    data = stream.read(chunk_size)
    frames.append(data)

print('Finished recording')


audio_data = b''.join(frames)
try:
    client_socket.sendall(audio_data)
    client_socket.send(b'END_OF_STREAM')
    print("Audio sent")
except ConnectionResetError:
    print("The connection was reset by the server. Retrying...")
    client_socket.close()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(audio_data)
    client_socket.send(b'END_OF_STREAM')

print("Please wait ")
text = client_socket.recv(1024).decode()
print('Text:', text)

client_socket.close()

