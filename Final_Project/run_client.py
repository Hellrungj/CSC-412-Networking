import sys
from CLIENT import Client

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
  TESTING = False
  sock = Client(HOST, PORT)
  sock.start_client()
  if TESTING == False:
    while True:
      user_input=raw_input(">")
      result = sock.parser(user_input)
      if not result == "ERROR":
        sock.send_recv(result)
  else:
    sock.TEST()

