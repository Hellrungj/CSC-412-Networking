# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import hashlib
from LOGGING import Logging

class Server():
  def __init__(self, host, port):
    self.server_address = (host, port)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    self.Log = Logging("server_log.txt")
    self.UD = {}
    self.MBX = {}
    self.IMQ = []    

  def start_server (self):
    self.Log.start_log()
    self.Log.file.write("{0} Server started\n".format(self.Log.log_time()))
    self.socket.bind(self.server_address)
    self.socket.listen(1)
    return socket

  def get_message (self):
    chars = []
    connection, client_address = self.socket.accept()
    self.Log.file.write("{1} Connect by {0}\n".format(client_address, self.Log.log_time()))
    print ("{1} Connection from [{0}]".format(client_address, self.Log.log_time()))
    try:
      while True:
        char = connection.recv(1) 
        if char == b'\0':
          break
        if char == b'':
          break
        else:
          chars.append(char.decode("utf-8") )
    finally:
      return (''.join(chars), connection)

  def stop_server (self):
    self.Log.file.write("{0 }Server stoped\n".format(self.Log.log_time()))
    self.Log.end_log()
    return self.socket.close()

  def is_login(self,user):
    print("{1} User: {0}".format(user, self.Log.log_time()))
    loginstatus = user[1]
    return loginstatus

  def data_part (self, data, index):
    try:
      return data.split(" ")[index]
    except:
      return False

  def ALA_service(self,count):
    if count >= 4:
      return True
    else:
      return False

  def generate_RSA(self):
    pass

  def handle_message (self,msg):
    if "CONNECT" in msg:
      return("OK", "Connection is good.")

    elif "LOGIN" in msg:
      username = msg.split(" ")[2]
      password = msg.split(" ")[3]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      UserData = self.UD[username]
      if UserData[0] != password:
        return("ERROR","Password invald")
      else:
        UserData[1] = True
        self.Log.file.write("{1} {0} login\n".format(username, 
						self.Log.log_time()))
        return("LOGIN", "{0} login".format(username))

    elif "LOGOUT" in msg:
      username = msg.split(" ")[2]
      password = msg.split(" ")[3]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      UserData = self.UD[username]
      if UserData[0] != password:
        return("ERROR","Password invald")
      UserData[1] = False
      self.Log.file.write("{1} {0} logout\n".format(username, 
						self.Log.log_time()))
      return("LOGOUT","{0} logout".format(username)) 
  
    elif "DUMP" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(self.UD[username]) == True:
        print(self.MBX)
        print(self.IMQ)
        self.Log.file.write("{1} {0} dumped MBX and IMQ\n".format(username,
							self.Log.log_time()))
        return ("OK", "\nMBX: {0}\nIMQ: {1}".format(self.MBX[username],self.IMQ))
      else:
        return ("Error", "Current user is not login")    

    elif "REGISTER" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) != None:
        return ("ERROR", "The user has already been registered")
      else:
        password = msg.split(" ")[3]
        self.UD[username] = [password,False]
        self.MBX[username] = []
        self.Log.file.write("{1} Registered {0}\n".format(username,
							self.Log.log_time()))
        return ("OK", "Register.")   

    elif "MESSAGE" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(self.UD[username]) == True:
        content = msg.split(" ")[3:]
        self.IMQ.insert(0, " ".join(content))
        self.Log.file.write("{1} {0} sent message\n".format(username, 
							self.Log.log_time()))
        return ("OK", "Sent message.")
      else:
        return ("ERROR", "Current user is not login")
    
    elif "STORE" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(self.UD[username]) == True:
        queued = self.IMQ.pop()
        print("Message in queue:\n---\n{0}\n---\n".format(queued))
        self.MBX[username].insert(0, queued)
        self.Log.file.write("{1} {0} stored a message\n".format(username, 
							self.Log.log_time()))
        return ("OK", "Stored message.")
      else:
        return ("ERROR", "Current user is not login")
    
    elif "COUNT" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(self.UD[username]) == True:
        self.Log.file.write("{1} {0} counted MBX\n".format(username, 
							self.Log.log_time()))
        return ("SEND", "COUNTED {0}".format(len(self.MBX[username])))
      else:
        return ("ERROR", "Current user is not login")

    elif "DELMSG" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(self.UD[username]) == True:
        self.MBX[username].pop(0)
        self.Log.file.write("{1} {0} deleted a message\n".format(username, 
							self.Log.log_time()))
        return ("OK", "Message deleted.")
      else:
        return ("Error", "Current user is not login")    

    elif "GETMSG" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(self.UD[username]) == True:
        first = self.MBX[username][0]
        self.Log.file.write("{1} {0} viewed a message\n".format(username,
							 self.Log.log_time()))
        print ("First message:\n---\n{0}\n---\n".format(first) )
        return ("SEND", first)
      else:
        return ("ERROR", "Current user is not login")

    elif "HELP" in msg:
      self.Log.file.write("{0} Help was requested\n".format(self.Log.log_time()))
      return ("Command List","\nFORMAT: (Name: Command)\nLOGIN: login <username>\nLOGOUT: logout <username>\nREGISTER: reg <username>\nDUMP: dump <username>\nMESSAGE: msg <username> <message>\nSTORE: store <username>\nCOUNT: count <username>\nDELMSG: delmsg <username>\nGETMSG: getmsg <username>")

    else:
      print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(msg))
      self.Log.file.write("{0} No Handler for client message\n".format(self.Log.log_time()))
      return ("ERROR", "No handler found for client message.")
