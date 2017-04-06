import os
import sys

class CommandLine():
  def __inti__(self):
    self.data = " "  
  
  def QUIT(self):
    sys.exit()

  def MKDIR(self,newpath):
    """ Creates a directory using filename or path """
    if not os.path.exists(newpath):
      os.makedirs(newpath)
      return "Created {0}.".format(newpath)
    else:
      return "ERROR: {0} already exists.".format(newpath) 

  def MKFILE(self,filename):
    """ Creates a file using a filename or path """
    # FIX ME: WILL NOT CREATE FILE 
    if not os.path.exists(filename):
      f= open(filename,"w+")
      f.close()
      return "Created {0}.".format(filename)
    else:
      return "ERROR: {0} already exists.".format(filename)

  def LIST(self):
    """ Prints out every file and directory in current directory """
    path = current_directory()
    result = ""
    for root, dirs, files in os.walk(path):
      #print("FILES: {0}".format(files))
      #print("+++")
      #print("DIRS: {0}".format(dirs))
      for i in dirs:
        files.append(i)
      S_files = sorted(files, key=str.lower)
      for file in S_files:
        #sys.stdout.write("{0} ".format(file))
        result += "{0}  ".format(file)
    return result 

  def PRINT(self,message):
    """ Print out to the screen a message """
    message = message.split(" ")
    del message[0]
    return " ".join(message)

  def MOVE(filename,directory):
    return "Moved: {0} to {1}".format(filename, directory)  

  def COPY(self,filename,new_filename):
    return "Copied: {0} to {1}".format(filename, new_filename)

  def ENTER(self,directory):
    return "Directory: {0}".format(directory)

  def MSG(self,data, index):
    return data.split(" ")[index]

  def current_directory(self):
    return os.path.dirname(os.path.abspath(__file__))  

  def check(self):
    """ Checks if the user input command and then calls the command functions """
    command =  self.data.split(" ")[0]
    command = command.lower()
    path = "/"
    if command == "quit" or command == "exit":
      return self.QUIT()
    elif command == "print" or command == "echo":
      return self.PRINT(data)
    elif command == "enter" or command == "cd":
      return self.ENTER(MSG(data, 1))
    elif command == "list" or command == "ls":
      return self.LIST()  
    elif command == "mkdir":
      return self.MKDIR(MSG(data, 1))
    elif command == "mkfile" or command == "touch":
      return self.MKFILE(MSG(data, 1))
    elif command == "move":
      return self.MOVE(MSG(data, 1), MSG(data, 2))
    elif command == "copy":
      return self.COPY(MSG(data, 1), MSG(data, 2))
    else:
      print("ERROR: No such command exist")

  def run():
    print("Welcome to Python Command Line:")
    while True:
      user_input=raw_input(">")
      print(self.check(user_input))    
    
