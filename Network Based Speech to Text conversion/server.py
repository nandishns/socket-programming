import socket
import struct
import sys
import wave
import os

import speech_recognition as sr

HOST = '192.168.223.117'  # Server IP address
# HOST = '127.0.0.1'  # local Host IP address
PORT = 5000


def process_audio(audio_data):

    with wave.open('audio.wav', 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.writeframes(audio_data)

    r = sr.Recognizer()
    with sr.AudioFile('audio.wav') as source:
        audio = r.record(source)
        print(audio, os.path.abspath('audio.wav'))

    text = ''
    try:
        text = r.recognize_google(audio)
        print("text:", text)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Speech recognition error: {0}".format(e))

    return text, os.path.abspath('audio.wav')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.bind((HOST, PORT))


server_socket.listen(1)

print('Waiting for a connection...')

while True:

    client_socket, address = server_socket.accept()
    print('Connected by', address)

    data = b''

    while True:
        packet = client_socket.recv(1024)
        if not packet:
            break
        if 'END_OF_STREAM' in packet.decode('utf-8', errors='ignore'):
            break
        data += packet

    print(data)

    text, file_path = process_audio(data)
    print(file_path)

    # with open(file_path, 'rb') as f:
    #     file_data = f.read()
    #     client_socket.sendall(file_data)

    print('Recognized text:', text)
    client_socket.send(text.encode())

    client_socket.close()
