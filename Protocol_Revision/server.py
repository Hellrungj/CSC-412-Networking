# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import sys
import time
import hashlib #For the checksum

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
# get_message : socket -> string
# Takes a socket and loops until it receives a complete message
# from a client. Returns the string we were sent.
# No error handling whatsoever.
def get_message (sock):
  chars = []
  connection, client_address = sock.accept()
  print ("Connection from [{0}]".format(client_address))
  try:
    while True:
      char = connection.recv(1) 
      if char == b'\0':
        break
      if char == b'':
        break
      else:
        # print("Appending {0}".format(char))
        chars.append(char.decode("utf-8") )
  finally:
    return (''.join(chars), connection)

# CONTRACT
# socket -> boolean
# Shuts down the socket we're listening on.
def stop_server (sock):
  return sock.close()

# DATA STRUCTURES
# The structures for your server should be defined and documented here.

# SERVER IMPLEMENTATION
# The implementation of your server should go here.
UD = {} #UserData  {<STR Username>:[<STR Password>,<BOOL LoginStatus>]}
MBX = {} #Mailbox  {<STR User>:<IMQ>}
IMQ = [] #Messages [<STR Message>]

def is_login(user):
  print("User: {0}".format(user))
  loginstatus = user[1]
  return loginstatus

def decode_md5(msg):
  #Decoded for the checksum
  return hashlib.md5(msg).hexdigest()

def checksum(msg):
  #MD5 verification
  msg_splited = msg.split(" ")
  chuck = msg_splited[0] #Grabs the Checksum chuck
  del msg_splited[0] #Deletes Checksum chuck
  rest_of_msg = " ".join(msg_splited)
  if chuck == decode_md5(rest_of_msg):
    return True
  else:
    return False

def data_part (data, index):
  # Slices the data and return selected uppercased sliced part 
  try:
    return data.split(" ")[index]
  except:
    return False

def ALA_service(count):
  #anti_login_attempt_service
  if count >= 4:
    return True
  else:
    return False

def md5(msg):
  #Checksum
  m = hashlib.md5()
  m.update(msg)
  return m.hexdigest()

def generate_RSA():
  pass

# CONTRACT
def handle_message (msg):
  if "LOGIN" in msg:
    #print("Message: {0}".format(msg))
    # Username
    username = msg.split(" ")[2]
    # Password
    password = msg.split(" ")[3]
    # IF the user is register status equals None?
    if UD.get(username) == None:
      #print("PASS")
      return("ERROR","User does not exsited")
    # ELIF the user is equal to the givin password
    UserData = UD[username]
    if UserData[0] != password:
      #print("USER")
      return("ERROR","Password invald")
    # ELSE login 
    else:
      #print("Login Status (B): {0}".format(UserData))
      UserData[1] = True
      #print("Login Status (F): {0}".format(UserData))
      return("LOGIN", "{0} login".format(username))

  elif "LOGOUT" in msg:
    username = msg.split(" ")[2]
    password = msg.split(" ")[3]
    if UD.get(username) == None:
      return("ERROR","User does not exsited")
    UserData = UD[username]
    if UserData[0] != password:
      return("ERROR","Password invald")
    UserData[1] = False
    return("LOGOUT","{0} logout".format(username)) 
  
  elif "DUMP" in msg:
    # Get the username
    username = msg.split(" ")[1]
    if self.UD.get(username) == None:
      return("ERROR","User does not exsited")
    if is_login(UD[username]) == True:
      print(MBX)
      print(IMQ)
      return ("OK", "Dumped.")
    else:
      return ("Error", "Current user is not login")    

  elif "REGISTER" in msg:
    # Get the username
    username = msg.split(" ")[2]
    # Get the password
    if UD.get(username) != None:
      return ("ERROR", "The user has already been registered")
    else:
      password = msg.split(" ")[3]
      # Create an empty list of messages
      UD[username] = [password,False]
      MBX[username] = []
      return ("OK", "Register.")   

  elif "MESSAGE" in msg:
    # Get the username
    username = msg.split(" ")[2]
    if self.UD.get(username) == None:
      return("ERROR","User does not exsited")
    #print("Username: {0}".format(username))
    if is_login(UD[username]) == True:
      # Get the content; slice everything after
      # the word MESSAGE
      content = msg.split(" ")[3:]
      # Put the content back together, and put 
      # it on the incoming message queue.
      IMQ.insert(0, " ".join(content))
      return ("OK", "Sent message.")
    else:
      return ("ERROR", "Current user is not login")
    
  elif "STORE" in msg:
    # Get the username
    username = msg.split(" ")[2]
    if self.UD.get(username) == None:
      return("ERROR","User does not exsited")
    if is_login(UD[username]) == True:
      queued = IMQ.pop()
      print("Message in queue:\n---\n{0}\n---\n".format(queued))
      MBX[username].insert(0, queued)
      return ("OK", "Stored message.")
    else:
      return ("ERROR", "Current user is not login")
    
  elif "COUNT" in msg:
    # Get the username
    username = msg.split(" ")[2]
    if self.UD.get(username) == None:
      return("ERROR","User does not exsited")
    if is_login(UD[username]) == True:
      return ("SEND", "COUNTED {0}".format(len(MBX[username])))
    else:
      return ("ERROR", "Current user is not login")

  elif "DELMSG" in msg:
    # Get the username
    username = msg.split(" ")[2]
    if self.UD.get(username) == None:
      return("ERROR","User does not exsited")
    if is_login(UD[username]) == True:
      MBX[username].pop(0)
      return ("OK", "Message deleted.")
    else:
      return ("Error", "Current user is not login")    

  elif "GETMSG" in msg:
    # Get the username
    username = msg.split(" ")[2]
    if self.UD.get(username) == None:
      return("ERROR","User does not exsited")
    if is_login(UD[username]) == True:
      first = MBX[username][0]
      print ("First message:\n---\n{0}\n---\n".format(first) )
      return ("SEND", first)
    else:
      return ("ERROR", "Current user is not login")

  elif "HELP" in msg:
    return ("SEND", "Command List:\nLOGIN: login <username>\nLOGOUT: logout <username>\nREGISTER: reg <username>\nDUMP: dump <username>\nMESSAGE: msg <username> <message>\nSTORE: store <username>\nCOUNT: count <username>\nDELMSG: delmsg <username>\nGETMSG: getmsg <username>")

  else:
    print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(msg))
    return ("ERROR", "No handler found for client message.")

if __name__ == "__main__":
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
  sock = start_server(host, port)
  print("Running server on host [{0}] and port [{1}]".format(host, port))
  
  RUNNING = True
  COUNTER = 0
  N = 0
  while RUNNING:
    if N == 0:
      message, conn = get_message(sock)
      #print("MESSAGE: [{0}]".format(message))
      if checksum(message):
        print("MESSAGE: [{0}]".format(message))  
        result, msg = handle_message(message)
      else:
        result, msg = ("ERROR","Data failed to transfer.")     
        print ("Result: {0}\nMessage: {1}\n".format(result, msg))
      if ALA_service(COUNTER):
        result = "ERROR"
        msg = "Too many attemps.\nNubmer Attempted: {0}\nPlease try again in one hour.\nThank you,\nServer.".format(COUNTER + 1)
        RUNNING = False
      elif result == "ERROR":
        CSmsg = "{0}: {1}".format(result, msg)
        #print("CSmsg: {0}".format(CSmsg))
        new_msg = md5(CSmsg)
        conn.sendall(bytes("{2} {0}: {1}\0".format(result,msg,new_msg)))
        COUNTER += 1
      else:
        CSmsg = "{0}: {1}".format(result, msg)
        #print("CSmsg: {0}".format(CSmsg))
        new_msg = md5(CSmsg)
        conn.sendall(bytes("{2} {0}: {1}\0".format(result,msg,new_msg)))
        COUNTER = 0
    else:
      print("'else' reached.")
      RUNNING = False
    conn.close()
  stop_server(sock)
