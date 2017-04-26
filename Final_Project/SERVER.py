# https://pymotw.com/2/socket/tcp.html
# https://docs.python.org/3/howto/sockets.html

# Messaging Server v0.1.0
import socket
import hashlib
from models import *
from LOGGING import Logging

class Server():
  def __init__(self, host, port):
    self.server_address = (host, port)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    self.Log = Logging("server_log.txt")    

  def start_server (self):
    self.Log.start_log()
    self.Log.file.write("{0} Server started\n".format(self.Log.log_time()))
    self.socket.bind(self.server_address)
    self.socket.listen(1)
    return self.socket

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
      self.Log.file.write("{0} {1} MSG:{2}\n".format(self.Log.log_time(),connection,''.join(chars)))
      return (''.join(chars), connection)

  def stop_server (self):
    self.Log.file.write("{0 }Server stoped\n".format(self.Log.log_time()))
    self.Log.end_log()
    return self.socket.close()

  def is_login(self, Username):
    print("{1} User: {0}".format(Username, self.Log.log_time()))
    loginstatus = User.select().where(User.username == Username).get()
    return loginstatus.login

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

  def CountMSG(self, Username):
    data = MailBox.select().where(MailBox.owner == Username).count()
    return data

  def Login(self, Username):
    data = User.select().where(User.username == Username).get()
    data.login = True
    data.save()

  def Logout(self, Username):
    data = User.select().where(User.username == Username).get()
    data.login = False
    data.save()

  def SaveRole(self, Name, Description ):
    data = Role(name = Name,
                description = Description)
    data.save()

  def SaveUser(self, Username, Password, Email):
    data = User(username = Username,
                password = Password,
                email = Email)
    data.save()

  def SaveUserRole(self, User, Role):
    data = User_Role(user = User,
                     role = Role)
    data.save()

  def SaveMSG(self, Owner, Sender, Title, Message):
    data = MailBox(owner = Owner,
                   sender = Sender,
		   title = Title,
		   message = Message)
    data.save()

  def DelMSG(self, Title):
    data = MailBox.select().where(MailBox.title == Title).get()
    data.delete_instance()

  def GetMessages(self):
    ListOfMessageData = []
    for data in MailBox.select():
      ListOfMessageData.append(("OWNER:",data.owner, 
				"SENDER:",data.sender,
				"TITLE:",data.title,
				"MESSAGE:",data.message))     
    return ListOfMessageData

  def GetUserRoles(self):
    ListOfMessageData = []
    for data in User_Role.select():
      ListOfMessageData.append(("USER:",data.user,
                                "ROLE:",data.role))
    return ListOfMessageData

  def GetRoles(self):
    ListOfMessageData = []
    for data in Role.select():
      ListOfMessageData.append(("NAME:",data.name,
                                "DESCRIPTION:",data.description))
    return ListOfMessageData

  def GetUsers(self):      
    ListOfUserData = []
    for data in User.select():
      ListOfUserData.append(("USERNAME:",data.username,
			     "PASSWORD:",data.password,
			     "EMAIL:",data.email,
			     "LOGIN:",data.login))
    return ListOfUserData

  def GetMSG(self, Title):
    data = MailBox.select().where(MailBox.title == Title).get()
    return data.message

  def UserRoleExist(self, Username, Role_Name):
    Userquery = User.select().where(User.username == Username)
    if not Userquery.exists():
      print("User does not exists.")
      return False
    Rolequery = Role.select().where(Role.name == Role_Name)
    if not Rolequery.exists():
      print("Role does not exists")
      return False
    data = User_Role.select().where(User_Role.user == Userquery,
				   User_Role.role == Rolequery) 
    return data.exists()

  def UserExist(self, Username): 
    query = User.select().where(User.username == Username)
    return query.exists()    

  def PasswordConfirmtion(self, Password):
    query = User.select().where(User.password == Password)
    print("Password:{0}".format(query))
    return query.exists()

  def handle_message (self,msg):
    if "CONNECT" in msg:
      self.Log.file.write("{0} Connected with Client\n".format(self.Log.log_time()))
      return("OK", "Connection is good.")

    elif "LOGIN" in msg:
      username = msg.split(" ")[2]
      password = msg.split(" ")[3]
      if not self.UserExist(username):
        self.Log.file.write("{0} {1} User Error\n".format(self.Log.log_time(),username))
        return("ERROR","User does not exsited")
      if not self.PasswordConfirmtion(password):
        self.Log.file.write("{0} {1} Loggin Error\n".format(self.Log.log_time(),username))
        return("ERROR","Password invald")
      else:
        self.Login(username)
        self.Log.file.write("{1} {0} login\n".format(username, 
						self.Log.log_time()))
        return("LOGIN", "{0} has successfully logged in.".format(username))

    elif "LOGOUT" in msg:
      username = msg.split(" ")[2]
      password = msg.split(" ")[3]
      if not self.UserExist(username):
        self.Log.file.write("{0} {1} Loggin Error\n".format(self.Log.log_time(),username))
        return("ERROR","User does not exsited")
      if not self.PasswordConfirmtion(password):
        self.Log.file.write("{0} {1} Loggin Error\n".format(self.Log.log_time(),username))
        return("ERROR","Password invald")
      else:
        self.Logout(username)      
        self.Log.file.write("{1} {0} logout\n".format(username, 
						self.Log.log_time()))
        return("LOGOUT","{0} has successfully logged in".format(username)) 
  
    elif "DUMP" in msg:
      username = msg.split(" ")[2]
      if not self.UserExist(username):
        self.Log.file.write("{0} {1} User Error\n".format(self.Log.log_time(),username))
        return("ERROR","User does not exsited")
      if not self.UserRoleExist(username, "Admin"):
        self.Log.file.write("{0} {1} Role Error\n".format(self.Log.log_time(),username))
        return("ERROR","You do not have premission to call this command")
      if self.is_login(username) == True:
        Messages = self.GetMessages()
        Users = self.GetUsers()
        Roles = self.GetRoles()
        UserRoles = self.GetUserRoles()
        print("User:{1}\nMSG:{0}".format(Messages,Users))
        self.Log.file.write("{1} {0} dumped MBX and Uesrs\n".format(username,
							self.Log.log_time()))
        return ("OK", "MBX: {0}\nUsers:{1}\nRoles:{2}\nUserRoles:{3}".format(Messages,
							Users, Roles, UserRoles))
      else:
        self.Log.file.write("{0} {1} Loggin Error\n".format(self.Log.log_time(),username))
        return ("Error", "Current user is not login")    

    elif "REGISTER" in msg:
      username = msg.split(" ")[2]
      if self.UserExist(username):
        self.Log.file.write("{0} {1} User Error\n".format(self.Log.log_time(),username))
        return ("ERROR", "The user has already been registered")
      else:
        password = msg.split(" ")[3]
        email = msg.split(" ")[4]
        self.SaveUser(username,password,email)
        self.Log.file.write("{1} {0} has successfully Registered\n".format(username,
							self.Log.log_time()))
        return ("OK", "Successfully Registered.")   

    elif "MESSAGE" in msg:
      username = msg.split(" ")[2]
      sender = msg.split(" ")[3]
      if not self.UserExist(username):
        self.Log.file.write("{0} {1} User Error\n".format(self.Log.log_time(),username))
        return("ERROR","User does not exsited")
      if not self.UserExist(sender):
        self.Log.file.write("{0} {1} Sender Error\n".format(self.Log.log_time(),username))
        return("ERROR","Sender does not exsited")      
      if self.is_login(username) == True:
        MSG = msg.split(";")[1]
        title = MSG.split(":")[0]
        content = MSG.split(":")[1:]
        self.SaveMSG(username, sender, title, " ".join(content))
        self.Log.file.write("{1} {0} sent message to {2}\n".format(username, 
							self.Log.log_time(),
							sender))
        return ("OK", "Sented message.")
      else:
        self.Log.file.write("{0} {1} Loggin Error\n".format(self.Log.log_time(),username))
        return ("ERROR", "Current user is not login")
    
    elif "COUNT" in msg:
      username = msg.split(" ")[2]
      if not self.UserExist(username):
        self.Log.file.write("{0} {1} User Error\n".format(self.Log.log_time(),username))
        return("ERROR","User does not exsited")
      if self.is_login(username) == True:
        self.Log.file.write("{1} {0} counted MBX\n".format(username, 
							self.Log.log_time()))
        return ("SEND", "Counted {0} message".format(self.CountMSG(username)))
      else:
        self.Log.file.write("{0} {1} Loggin Error\n".format(self.Log.log_time(),username))
        return ("ERROR", "Current user is not login")

    elif "DELMSG" in msg:
      username = msg.split(" ")[2]
      if not self.UserExist(username):
        return("ERROR","User does not exsited")
        self.Log.file.write("{0} {1} User Error\n".format(self.Log.log_time(),username))
      if self.is_login(username) == True:
        title = msg.split(" ")[3:]
        self.DelMSG(title)
        self.Log.file.write("{1} {0} deleted a message\n".format(username, 
							self.Log.log_time()))
        return ("OK", "Message deleted.")
      else:
        self.Log.file.write("{0} {1} Loggin Error\n".format(self.Log.log_time(),username))
        return ("Error", "Current user is not login")    

    elif "GETMSG" in msg:
      username = msg.split(" ")[2]
      if not self.UserExist(username):
        return("ERROR","User does not exsited")
        self.Log.file.write("{0} {1} User Error\n".format(self.Log.log_time(),username))
      if self.is_login(username) == True:
        restMSG = msg.split(" ")[3:]
        title = " ".join(restMSG) 
        print("Title:{0}".format(title))
        message = self.GetMSG(title)
        self.Log.file.write("{1} {0} viewed a message\n".format(username,
							 self.Log.log_time()))
        print ("First message:\n---\n{0}\n---\n".format(message) )
        return ("SEND", message)
      else:
        self.Log.file.write("{0} {1} Loggin Error\n".format(self.Log.log_time(),username))
        return ("ERROR", "Current user is not login")

    elif "HELP" in msg:
      self.Log.file.write("{0} Help was requested\n".format(self.Log.log_time()))
      return ("Command List","\nLOGIN: login <username>\nLOGOUT: logout <username>\nREGISTER: reg <username>\nDUMP: dump <username>\nMESSAGE: msg <username>\nCOUNT: count <username>\nDELMSG: delmsg <username>\nGETMSG: getmsg <username>\nTESTFILE: test <filename>")

    else:
      print("NO HANDLER FOR CLIENT MESSAGE: [{0}]".format(msg))
      self.Log.file.write("{0} No Handler for client message\n".format(self.Log.log_time()))
      return ("ERROR", "No handler found for client message.")
