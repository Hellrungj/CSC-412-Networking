# Messaging Client
import socket
import sys
import hashlib #For the checksum

MSGLEN = 1

class Client():
  def __init__(self, host, port):
    self.server_address = (host, port)

  def receive_message(self):
    chars = []
    try:
      while True:
        char = self.socket.recv(1)
        if char == b'\0':
          break
        if char == b'':
          break
        else:
          #print("Appending {0}".format(char))
          chars.append(char.decode("utf-8"))
    finally:
      return ''.join(chars)

  def send(self, msg):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect(self.server_address)
    msg = "{1} {0}".format(msg,self.md5(msg)) #Checksum
    length = self.socket.send(bytes(msg + "\0"))
    print ("SENT MSG: '{0}'".format(msg))
    print ("CHARACTERS SENT: [{0}]".format(length))

  def recv(self):
    response = self.receive_message()
    #print("ORGIANAL RESPONSE: {0}".format(response))
    if not self.checksum(response):
      response = ("ERROR","Data failed to transfer.")
    print("RESPONSE: [{0}]".format(response))
    self.socket.close()
    return response

  def send_recv (self,msg):
    self.send(msg)
    response = self.recv()
    self.resend(response, msg)

  def md5(self, msg):
    #Checksum
    m = hashlib.md5()
    m.update(msg)
    return m.hexdigest()
 
  def decode_md5(self, msg):
    #Decoded for the checksum
    return hashlib.md5(msg).hexdigest()

  def checksum(self, msg):
    #MD5 verification
    msg_splited = msg.split(" ")
    chuck = msg_splited[0]      #Grabs the Checksum chuck
    del msg_splited[0]          #Deletes Checksum chuck
    rest_of_msg = " ".join(msg_splited)
    #print("CHUCK: {0}".format(chuck))
    #print("REST: {0}".format(rest_of_msg))
    #print("DECODE: {0}".format(decode_md5(rest_of_msg)))
    if chuck == self.decode_md5(rest_of_msg):
      return True
    else:
      return False

  def resend (self, response, msg):
    if self.data_part(response,0) == "ERROR:":
      UI = raw_input("Do you want to resend the mesage?(y/n)")
      if UI.lower() == "y" or UI.lower() == "yes":
        print ("__RESENDING__")
        self.send_recv(msg)

  def data_part (self, data, index):
    # Slices the data and return selected uppercased sliced part 
    #print("Data: {0}, Index: {1}".format(data,index))
    try:
      return data.split(" ")[index]
    except:
      return False

  def MSG (self, data):
     message = data.split(" ")
     del message[0] #Deletes Command
     del message[0] #Deletes Username
     return " ".join(message)

  def confirm(self, password, password2):
    if password == password2:
      return True
    else:
      return False

  def check(self, data):
    """ Checks if the user input command and then calls the command functions """
    command = self.data_part(data, 0)
    if command == False:
      print("ERROR: No command given.")
    else:
      command = command.upper()
      if command == "REGISTER" or command == "REG":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("REGISTER <username> or REG <username>")
          return("ERROR")
        else:
          password = raw_input("Create password:")
          conf_pass = raw_input("Confirm password:")
          if self.confirm(password, conf_pass) == True:
            return "REGISTER {username} {password}".format(username=self.data_part(data,1),
                                                          password=password)
          else:
            print("Your passwords is not same")
            return("ERROR")
      elif command == "LOGIN":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("LOGIN <username>")
          return("ERROR")
        else:
          password = raw_input("Password:")
          return "LOGIN {username} {password}".format(username=self.data_part(data,1),
                                                          password=password)
      elif command == "LOGOUT":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("LOGOUT: username")
          return("ERROR")
        else:
          password = raw_input("Password:")
          return "LOGOUT {username} {password}".format(username=self.data_part(data,1),
                                                        password=password)
      elif command == "MSG":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("MSG: <username> <message>")
          return("ERROR")
        else:
          return "MESSAGE {username} {message}.".format(username=self.data_part(data,1),
                                                        message=self.MSG(data))  
      elif command == "DUMP":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("DUMP: <username>")
          return("ERROR")
        else:
          return "DUMP {username}".format(username=self.data_part(data,1))
      elif command == "STORE":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("STORE: <username>")
          return("ERROR")
        else:
          return "STORE {username}".format(username=self.data_part(data,1))
      elif command == "COUNT":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("COUNT: <username>")
          return("ERROR")
        else:
          return "COUNT {username}".format(username=self.data_part(data,1))
      elif command == "GETMSG":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("GETMSG: <username>")
          return("ERROR")
        else:
          return "COUNT {username}".format(username=self.data_part(data,1))
      elif command == "GETMSG":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("GETMSG: <username>")
          return("ERROR")
        else:
          return "GETMSG {username}".format(username=self.data_part(data,1))
      elif command == "DELMSG":
        if self.data_part(data,1) == False:
          print("Usage:")
          print("DELMSG: <username>")
          return("ERROR")
        else:
          return "DELMSG {username}".format(username=self.data_part(data,1))
      elif command == "EXIT" or command == "QUIT":
        sys.exit()
      elif command == "TEST":
        TEST()
      elif command == "HELP":
        return "HELP"
      else:
        print("ERROR: No such command exist")
        return("ERROR")

  def TEST(self):
    # FIX ME: make this file
    pass


