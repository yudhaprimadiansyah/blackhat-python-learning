import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

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
                                                            '''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=1234, help='specified port')
    parser.add_argument("-t", "--upload", help='Upload File')
    args = parser.parse_args()