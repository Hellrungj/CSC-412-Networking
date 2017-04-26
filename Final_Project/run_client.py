import sys
import random
from CLIENT import Client

def client_setup(host,port_range):
  port = port_range[0]
  try:
    sock = Client(host, port)
    sock.start_client()
    return sock
  except:
    new_port = random.choice(port_range)
    if new_port == port:
      new_port = random.choice(port_range)
      sock = Client(host, new_port)
      sock.start_client()
      return sock
    else:
      sock = Client(host, new_port)
      sock.start_client()      
      return sock

def get_host_port():
  # Check if the user provided all of the 
  # arguments. The script name counts
  # as one of the elements, so we need at 
  # least three, not fewer.
  if len(sys.argv) < 2:
    print ("Usage: ")
    print (" python server.py <host> <port>")
    print (" e.g. python server.py localhost 8888")
    print
    sys.exit()
  host = sys.argv[1]
  port = int(sys.argv[2])
  addesss_info = (host, port)
  return address_info

if __name__ == "__main__":
  HOST = 'localhost'
  PORT = 8888
  #(HOST, PORT) = get_host_port()
  sock = client_setup(HOST, (PORT,PORT+100))
  while True:
    user_input=raw_input(">")
    result = sock.interpret(user_input)
    if "TEST" in result.split(" ")[0]:
      sock.Test(result.split(" ")[1])
    elif not result == "ERROR":
      sock.send_recv(result)

