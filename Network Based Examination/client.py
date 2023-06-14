import socket

def start_client():
    host = "127.0.0.1"
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Send the registration number to the server
        reg_number = input("Enter your registration number: ")
        s.sendall(reg_number.encode())

        # Receive and answer the exam questions
        for i in range(3):
            question = s.recv(1024).decode()
            print(question)
            answer = input("Your answer: ")
            s.sendall(answer.encode())

if __name__ == "__main__":
    start_client()
