import socket

server_address = ('', 12345)
sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)

while True:
  connection, client_address = sock.accept()
  try:
    while True:
      data = sock.recv(1024)
      if data:
        print("Received: {0}\n".format(data))
      else:
        break
  finally:
    sock.close()
