# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import hashlib

class Server():
  def __init__(self, host, port):
    self.server_address = (host, port)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.filename = "Log.txt"
    self.file = None
    self.UD = {}
    self.MBX = {}
    self.IMQ = [] 

  def start_server (self):
    socket.bind(self.server_address)
    socket.listen(1)
    return socket

  def get_message (self):
    chars = []
    connection, client_address = self.socket.accept()
    print ("Connection from [{0}]".format(client_address))
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
    return self.socket.close()

  def is_login(self,user):
    print("User: {0}".format(user))
    loginstatus = user[1]
    return loginstatus

  def decode_md5(self,msg):
    return hashlib.md5(msg).hexdigest()

  def checksum(msg):
    msg_splited = msg.split(" ")
    chuck = msg_splited[0]
    del msg_splited[0] 
    rest_of_msg = " ".join(msg_splited)
    if chuck == decode_md5(rest_of_msg):
      return True
    else:
      return False

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

  def md5(self,msg):
    m = hashlib.md5()
    m.update(msg)
    return m.hexdigest()

  def generate_RSA(self):
    pass

  def handle_message (self,msg):
    if "LOGIN" in msg:
      username = msg.split(" ")[2]
      password = msg.split(" ")[3]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      UserData = self.UD[username]
      if self.UserData[0] != password:
        return("ERROR","Password invald")
      else:
        self.UserData[1] = True
        return("LOGIN", "{0} login".format(username))

    elif "LOGOUT" in msg:
      username = msg.split(" ")[2]
      password = msg.split(" ")[3]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      UserData = self.UD[username]
      if self.UserData[0] != password:
        return("ERROR","Password invald")
      self.UserData[1] = False
      return("LOGOUT","{0} logout".format(username)) 
  
    elif "DUMP" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(UD[username]) == True:
        print(self.MBX)
        print(self.IMQ)
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
        return ("OK", "Register.")   

    elif "MESSAGE" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(UD[username]) == True:
        content = msg.split(" ")[3:]
        self.IMQ.insert(0, " ".join(content))
        return ("OK", "Sent message.")
      else:
        return ("ERROR", "Current user is not login")
    
    elif "STORE" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(UD[username]) == True:
        queued = self.IMQ.pop()
        print("Message in queue:\n---\n{0}\n---\n".format(queued))
        self.MBX[username].insert(0, queued)
        return ("OK", "Stored message.")
      else:
        return ("ERROR", "Current user is not login")
    
    elif "COUNT" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(UD[username]) == True:
        return ("SEND", "COUNTED {0}".format(len(self.MBX[username])))
      else:
        return ("ERROR", "Current user is not login")

    elif "DELMSG" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(UD[username]) == True:
        self.MBX[username].pop(0)
        return ("OK", "Message deleted.")
      else:
        return ("Error", "Current user is not login")    

    elif "GETMSG" in msg:
      username = msg.split(" ")[2]
      if self.UD.get(username) == None:
        return("ERROR","User does not exsited")
      if self.is_login(UD[username]) == True:
        first = self.MBX[username][0]
        print ("First message:\n---\n{0}\n---\n".format(first) )
        return ("SEND", first)
      else:
        return ("ERROR", "Current user is not login")

    elif "HELP" in msg:
      return ("SEND", "Command List:\nLOGIN: login <username>\nLOGOUT: logout <username>\nREGISTER: reg <username>\nDUMP: dump <username>\nMESSAGE: msg <username> <message>\nSTORE: store <username>\nCOUNT: count <username>\nDELMSG: delmsg <username>\nGETMSG: getmsg <username>")

    else:
      print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(msg))
      return ("ERROR", "No handler found for client message.")
