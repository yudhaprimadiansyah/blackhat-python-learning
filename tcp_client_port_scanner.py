import socket

host = "twitter.com"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for x in range(0,1000):
    try:
        client.connect((host, x))
        client.close()
        print("Port {0} is Open".format(x))
    except:
        print("Port {0} is closed".format(x))
        continue