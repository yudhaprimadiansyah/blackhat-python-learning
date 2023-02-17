import socket

host = "twitter.com"
port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

client.send(b"GET / HTTP/1.1\r\nHost: twitter.com\r\n\r\nCustom-Header: lol lmao")
resp = client.recv(4096)
data = resp.decode().split("\n")
print("Response Status : {0}".format(data[0]))
client.close()