import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


class SimpleNetCat:
    def __init__(self, args, buf=None): # Constructor
        self.args = args
        self.buf = buf
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
            
    def send(self):
        buf_size = 4096
        self.socket.connect((self.args.target, self.args.port))
        if self.buf:
            self.socket.send(self.buf)
            
        try:
            while True:
                recv_length = 1
                response = ''
                while recv_length:
                    data = self.socket.recv(buf_size)
                    recv_length = len(data)
                    response += data.decode()
                    if recv_length < buf_size:
                        print(response)
                        buf = input('> ')
                        buf += "\n"
                        self.socket.send(buf.encode())
        except:
            print("Connection Terminated")
            self.socket.close()
            sys.exit()
            
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client,addr = self.socket.accept()
            handler = threading.Thread(target=self.client_handle, args=(client,))
            handler.start()
    
    def client_handle(self, client_socket):
        if self.args.execute:
            output = exec(self.args.execute)
            client_socket.send(output.encode())
        
        elif self.args.upload:
            file_buf = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buf += data
                else:
                    break
                
            with open(self.args.upload, 'wb') as wf:
                wf.write(file_buf)
            message = f'File Saved as {self.args.upload}'
            client_socket.send(message.encode())
            
        elif self.args.command:
            cmd_buf = b''
            while True:
                try:
                    client_socket.send(b'Cepot: #> ')
                    while '\n' not in cmd_buf.decode():
                        cmd_buf += client_socket.recv(128)
                    resp = exec(cmd_buf.decode())
                    if resp:
                        client_socket.send(resp.encode())
                    cmd_buf = b''
                except Exception as e:
                    print(f"server killed {e}")
                    self.socket.close()
                    sys.exit() 

                    

def exec(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output =  subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT) # Use check_output to run local command system shell and return the output to variable output
    return output.decode()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Yupwn Simple Netcat (Practice Purposes)",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''
                                                            simple_netcat.py -t 192.168.1.1 -p 1234 -l -c # command Shell
                                                            simple_netcat.py -t 192.168.1.1 -p 1234 -l -u=data.txt # Send File
                                                            simple_netcat.py -t 192.168.1.1 -p 1234 -l -e=\"ls -la\" # Execute Command
                                                            echo "Yudha Ganteng" | simple_netcat.py -t 192.168.1.1 -p 1234 # Echo data to server
                                                            simple_netcat.py -t 192.168.1.1 -p 1234 # Connect to server
                                                            ''')) # argparse is an standard module in python. use it to define parameters configuration
    parser.add_argument('-c', '--command', action='store_true', help='command shell') # Setup argument configuration for the parser
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=1234, help='specified port')
    parser.add_argument("-t", "--target", default="127.0.0.1", help='Specified IP')
    parser.add_argument("-u", "--upload", help="Upload File")
    args = parser.parse_args()
    if args.listen: # Set it up as Listener
        buf = ''
    else:
        buf = sys.stdin.read()
    nc = SimpleNetCat(args, buf.encode())
    nc.run()
    
    

