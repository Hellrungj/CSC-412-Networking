# Messaging Client
import socket
import sys

MSGLEN = 1

# CONTRACT
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def receive_message (sock):
  data = sock.recv(1024)
  message=""
  for i in data:
    if b'\0'== i:
      pass
    if b' '==i:
      pass
    if "H"==i or "E"==i or "L"==i or "O"==i:
      message+=i
  return message

if __name__ == "__main__":
  # Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  if len(sys.argv) < 3:
    print ("Usage:")
    print (" python client.py <host> <port>")
    print (" For example:")
    print (" python client.py localhost 8888")
    print 
    sys.exit()

  host = sys.argv[1]
  port = int(sys.argv[2])
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((sys.argv[1], int(sys.argv[2])))

  chars_sent = sock.send(b"HELO\0")
  print ("CHARACTERS SENT: [{0}]".format(chars_sent))

  response = receive_message(sock)
  print("RESPONSE: [{0}]".format(response))

  sock.close()
