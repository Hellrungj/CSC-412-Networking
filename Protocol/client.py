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
  chars = []
  try:
    while True:
      char = sock.recv(1)
      if char == b'\0':
        break
      if char == b'':
        break
      else:
        # print("Appending {0}".format(char))
        chars.append(char.decode("utf-8") )
  finally:
    return ''.join(chars)
  
def send (msg):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((HOST, PORT))
  length = sock.send(bytes(msg + "\0"))
  print ("SENT MSG: '{0}'".format(msg))
  print ("CHARACTERS SENT: [{0}]".format(length))
  return sock

def recv (sock):
  response = receive_message(sock)
  print("RESPONSE: [{0}]".format(response))
  sock.close()  

def send_recv (msg):
  recv(send(msg))
  

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

  HOST = sys.argv[1]
  PORT = int(sys.argv[2])

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((HOST, PORT))
  length = sock.send(b"DUMP\0")
  print ("CHARACTERS SENT: [{0}]".format(length))
  response = receive_message(sock)
  print("RESPONSE: [{0}]".format(response))
  sock.close()

  # I don't want to copy paste everything above.
  # So, I put it in a function or two.
  s =send("REGISTER <hellrungj> <Natioh22>")
  send_recv("REGISTER <praters> <zackfair>")
  send_recv("LOGIN <hellrungj> <Natioh22>")
  send_recv("MESSAGE <hellrungj> Four score and seven years ago.")
  send_recv("DUMP <hellrungj>")
  send_recv("STORE <hellrungj>")
  send_recv("COUNT <hellrungj>")
  send_recv("GETMSG <hellrungj>")
  send_recv("DELMSG <hellrungj>")
  print(" ")
  print(" Login - Logout Testing ")
  send_recv("LOGIN <hellr> <Natioh22>")
  send_recv("LOGIN <hellrungj> <Nati>")
  send_recv("LOGIN <hellrungj> <Natioh22>")
  send_recv("LOGOUT <hellrungj> <Natioh22>")
  send_recv("LOGOUT <praters> <zackfair>")
  #s = send("LOGIN <praters> <fairzack>")
  #s = send("REGISTER <praters> <zackfair>")
  #s = send("MESSAGE <hellrungj>")
 
 #
 #  recv(send("DUMP"))
 #  #recv(send("GETMSG jadudm"))
 #  #recv(send("DELMSG jadudm"))
