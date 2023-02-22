import socket
import threading


host = "0.0.0.0"
port = 11300


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port)) #setup server host and port
    server.listen(5) # listen with maximum 5 backlog connection
    print(f"[*] Service Listening on {host}:{port}")
    
    
    while True:
        client,addr = server.accept() #accept client connection and put it to client variable with its addres information to addr
        print(f"[*] Accepted Connection coming from : {addr[0]}:{addr[1]}")
        handler = threading.Thread(target=handle_client_conn,args=(client,))
        handler.start() # Create and start Thread object that handle connection via handle_client_cont with argument client
        

def handle_client_conn(client): # Handle Client Request
    with client as sock:
        req = sock.recv(4096)
        print(f'[*] Received : {req.decode("utf-8")}')
        sock.send(b"ACK")
        
if __name__ == "__main__":
    main()