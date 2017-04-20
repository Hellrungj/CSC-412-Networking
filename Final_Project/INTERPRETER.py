class Interpreter():
  def __init__(self, data):
    self.data = data 

  def data_part (self, index):
    # Slices the data and return selected uppercased sliced part 
    #print("Data: {0}, Index: {1}".format(data,index))
    try:
      return self.data.split(" ")[index]
    except:
      return False

  def MSG (self):
     message = self.data.split(" ")
     del message[0] #Deletes Command
     del message[0] #Deletes Username
     return " ".join(message)

  def confirm(self, password, password2):
    if password == password2:
      return True
    else:
      return False

  def check(self):
    """ Checks if the user input command and then calls the command functions """
    command = self.data_part(0)
    if command == False:
      print("ERROR: No command given.")
    else:
      command = command.upper()
      if command == "REGISTER" or command == "REG":  
        if self.data_part(1) == False:
          print("Usage:")
          print("REGISTER <username> or REG <username>")
          return("ERROR")
        else:
          password = raw_input("Create password:")
          conf_pass = raw_input("Confirm password:")
          if self.confirm(password, conf_pass) == True:
            return "REGISTER {username} {password}".format(username=self.data_part(1),
                                                          password=password)
          else:
            print("Your passwords is not same")
            return("ERROR")

      elif command == "LOGIN":
        if self.data_part(1) == False:
          print("Usage:")
          print("LOGIN <username>")
          return("ERROR")
        else:
          password = raw_input("Password:")
          return "LOGIN {username} {password}".format(username=self.data_part(1),
                                                          password=password)

      elif command == "LOGOUT":
        if self.data_part(1) == False:
          print("Usage:")
          print("LOGOUT: username")
          return("ERROR")
        else:
          password = raw_input("Password:")
          return "LOGOUT {username} {password}".format(username=self.data_part(1),
                                                        password=password)

      elif command == "MSG":
        if self.data_part(1) == False:
          print("Usage:")
          print("MSG: <username> <message>")
          return("ERROR")
        else:
          return "MESSAGE {username} {message}.".format(username=self.data_part(1),
                                                        message=self.MSG())

      elif command == "DUMP":
        if self.data_part(1) == False:
          print("Usage:")
          print("DUMP: <username>")
          return("ERROR")
        else:
          return "DUMP {username}".format(username=self.data_part(1))

      elif command == "STORE":
        if self.data_part(1) == False:
          print("Usage:")
          print("STORE: <username>")
          return("ERROR")
        else:
          return "STORE {username}".format(username=self.data_part(1))

      elif command == "COUNT":
        if self.data_part(1) == False:
          print("Usage:")
          print("COUNT: <username>")
          return("ERROR")
        else:
          return "COUNT {username}".format(username=self.data_part(1))

      elif command == "GETMSG":
        if self.data_part(1) == False:
          print("Usage:")
          print("GETMSG: <username>")
          return("ERROR")
        else:
          return "GETMSG {username}".format(username=self.data_part(1))

      elif command == "DELMSG":
        if self.data_part(1) == False:
          print("Usage:")
          print("DELMSG: <username>")
          return("ERROR")
        else:
          return "DELMSG {username}".format(username=self.data_part(1))

      elif command == "EXIT" or command == "QUIT":
        return "EXIT"

      elif command == "TEST":
        TEST()

      elif command == "HELP":
        return "HELP"

      else:
        print("ERROR: No such command exist")
        return("ERROR")
