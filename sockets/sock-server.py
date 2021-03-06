#
# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import sys


# CONTRACT
# start_server : string number -> socket
# Takes a hostname and port number, and returns a socket
# that is ready to listen for requests
def start_server (host, port):
  server_address = (host, port)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(server_address)
  sock.listen(1)
  return sock
  
# CONTRACT
# get_message : socket -> Tuple(string, socket)
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def get_message (sock):
  conn, addr = sock.accept()
  data = conn.recv(1024)
  message=""
  for i in data:
    if b'\0'== i:
      pass
    if b' '==i:
      pass
    if "H"==i or "E"==i or "L"==i or "O"==i:
      message+=i
  return (message, conn)

# CONTRACT
# socket -> boolean
# Shuts down the socket we're listening on.
def stop_server (sock):
  return sock.close()

# CONTRACT
# handle_message : string socket -> boolean
# Handles the message, and returns True if the server
# should keep handling new messages, or False if the 
# server should shut down the connection and quit.
def handle_message (msg, conn):
  return False
  
if __name__ == "__main__":
  # Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  if len(sys.argv) < 3:
    print ("Usage: ")
    print (" python server.py <host> <port>")
    print (" e.g. python server.py localhost 8888")
    print 
    sys.exit()

  host = sys.argv[1]
  port = int(sys.argv[2])
  sock = start_server(host, port)
  print("Running server on host [{0}] and port [{1}]".format(host, port))
  
  RUNNING = True
  while RUNNING:
    message, connection = get_message(sock)
    print("MESSAGE: [{0}]".format(message))
    RUNNING = handle_message(message, connection)
    # This 'if' probably should not be in production.
    # Our template/test code returns "None" for the connection...
    if connection:
      connection.close()
    
  stop_server(sock)
