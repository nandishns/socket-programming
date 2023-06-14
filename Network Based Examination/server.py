import socket
import threading
import ssl

def handle_client(conn, addr):
    reg_number = conn.recv(1024).decode()
    password = conn.recv(1024).decode()

    if verify_credentials(reg_number, password):
        success = "You have successfully Signed"
        conn.sendall(success.encode())
       
        questions = [
            "What is the capital of France?",
            "What is the largest continent?",
            "What is the currency of Japan?",
        ]
        for question in questions:
            conn.sendall(question.encode())
            answer = conn.recv(1024).decode()
            
            with open("exam_results.txt", "a") as f:
                f.write(f"{reg_number},{answer}\n")
                
        conn.sendall("Your Examination is completed. All the best for your result.".encode())    
    else:
        status = "Register number or Password is invalid"
        conn.sendall(status.encode())
    
    conn.close()

def verify_credentials(reg_number, password):
    if password == "1@3":
        return True

def start_server():
    host = "192.168.113.117"
    port = 12345

    certfile = "example.crt"  
    keyfile = "example.key"  

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        
        print("Server Started. Waiting for the connection")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.verify_mode = ssl.CERT_NONE
            context.load_cert_chain(certfile, keyfile)
            print(context)
            
            conn = context.wrap_socket(conn, server_side=True)
            
            # Start a new thread to handle the client
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    start_server()
