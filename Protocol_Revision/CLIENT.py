# Messaging Client
import socket
import sys
import hashlib #For the checksum

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
  msg = "{1} {0}".format(msg,md5(msg)) #Checksum
  length = sock.send(bytes(msg + "\0"))
  print ("SENT MSG: '{0}'".format(msg))
  print ("CHARACTERS SENT: [{0}]".format(length))
  return sock

def recv (sock):
  response = receive_message(sock)
  #print("ORGIANAL RESPONSE: {0}".format(response))
  if not checksum(response):
    response = ("ERROR","Data failed to transfer.")
  print("RESPONSE: [{0}]".format(response))
  sock.close()  
  return response
 
def send_recv (msg):
  response = recv(send(msg))
  resend(response, msg)

def md5(msg):
  #Checksum
  m = hashlib.md5()
  m.update(msg)
  return m.hexdigest()

def decode_md5(msg):
  #Decoded for the checksum
  return hashlib.md5(msg).hexdigest()

def checksum(msg):
  #MD5 verification
  msg_splited = msg.split(" ")
  chuck = msg_splited[0] #Grabs the Checksum chuck
  del msg_splited[0] #Deletes Checksum chuck
  rest_of_msg = " ".join(msg_splited)
  #print("CHUCK: {0}".format(chuck))
  #print("REST: {0}".format(rest_of_msg))
  #print("DECODE: {0}".format(decode_md5(rest_of_msg)))
  if chuck == decode_md5(rest_of_msg):
    return True
  else:
    return False

def resend (response, msg):
  if data_part(response,0) == "ERROR:":
    UI = raw_input("Do you want to resend the mesage?(y/n)")
    if UI.lower() == "y" or UI.lower() == "yes":
      print ("__RESENDING__")
      send_recv(msg)

def data_part (data, index):
  # Slices the data and return selected uppercased sliced part 
  try:
    return data.split(" ")[index]
  except:
    return False

def MSG (data):
   message = data.split(" ")
   del message[0] #Deletes Command
   del message[0] #Deletes Username
   return " ".join(message)

def confirm(password, password2):
  if password == password2:
    return True
  else:
    return False

def check(data):
  """ Checks if the user input command and then calls the command functions """
  command = data_part(data, 0)
  command = command.upper()
  if command == "REGISTER" or command == "REG":
    if data_part(data,1) == False:
      print("Usage:")
      print("REGISTER <username> or REG <username>")
      return("ERROR")
    else:
      password = raw_input("Create password:")
      conf_pass = raw_input("Confirm password:")
      if confirm(password, conf_pass) == True: 
        return "REGISTER {username} {password}".format(username=data_part(data,1),
    							password=password)
      else:
        print("Your passwords is not same")					
        return("ERROR")

  elif command == "LOGIN":
    if data_part(data,1) == False:
      print("Usage:")
      print("LOGIN <username>")
      return("ERROR")
    else:
      password = raw_input("Password:")
      return "LOGIN {username} {password}".format(username=data_part(data,1),
                                                        password=password)
  elif command == "LOGOUT":
    if data_part(data,1) == False:
      print("Usage:")
      print("LOGOUT: username")
      return("ERROR")
    else:
      password = raw_input("Password:")
      return "LOGOUT {username} {password}".format(username=data_part(data,1),
                                                        password=password)
  elif command == "MSG":
    if data_part(data,1) == False:
      print("Usage:")
      print("MSG: <username> <message>")
      return("ERROR")
    else:
      return "MESSAGE {username} {message}.".format(username=data_part(data,1),
							message=MSG(data))
  elif command == "DUMP":
    if data_part(data,1) == False:
      print("Usage:")
      print("DUMP: <username>")
      return("ERROR")
    else:
      return "DUMP {username}".format(username=data_part(data,1))
  elif command == "STORE":
    if data_part(data,1) == False:
      print("Usage:")
      print("STORE: <username>")
      return("ERROR")
    else:
      return "STORE {username}".format(username=data_part(data,1))
  elif command == "COUNT":
    if data_part(data,1) == False:
      print("Usage:")
      print("COUNT: <username>")
      return("ERROR")
    else:
      return "COUNT {username}".format(username=data_part(data,1))
  elif command == "GETMSG":
    if data_part(data,1) == False:
      print("Usage:")
      print("GETMSG: <username>")
      return("ERROR")
    else:
      return "GETMSG {username}".format(username=data_part(data,1))
  elif command == "DELMSG":
    if data_part(data,1) == False:
      print("Usage:")
      print("DELMSG: <username>")
      return("ERROR")
    else:
      return "DELMSG {username}".format(username=data_part(data,1))
  elif command == "EXIT" or command == "QUIT":
    sys.exit()
  elif command == "TEST":
    TEST()
  elif command == "HELP":
    return "HELP"
  else:
    print("ERROR: No such command exist")
    return("ERROR")

def TEST():
  # FIX ME: make this file
  print("Running Test")
  print("__GENERAL__")
  send_recv("REGISTER <hellrungj> <Natioh22>")
  send_recv("REGISTER <praters> <zackfair>")
  send_recv("LOGIN <hellrungj> <Natioh22>")
  send_recv("MESSAGE <hellrungj> Four score and seven years ago.")
  send_recv("DUMP <hellrungj>")
  send_recv("STORE <hellrungj>")
  send_recv("COUNT <hellrungj>")
  send_recv("GETMSG <hellrungj>")
  send_recv("DELMSG <hellrungj>")
  print("__AUTHCATION__")
  send_recv("LOGIN <hellr> <Natioh22>")
  send_recv("LOGIN <hellrungj> <Nati>")
  send_recv("LOGIN <hellrungj> <Natioh22>")
  send_recv("LOGOUT <hellrungj> <Natioh22>")
  send_recv("LOGOUT <praters> <zackfair>")
  send_recv("LOGIN <praters> <fairzack>")  

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
  
  if TESTING == False:
    while True:
      user_input=raw_input(">")
      result = check(user_input)
      if not result == "ERROR":
        send_recv(result)
  else:
    TEST()
