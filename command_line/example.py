import os
import sys

def QUIT():
  sys.exit()

def MKDIR(newpath):
  """ Creates a directory using filename or path """
  if not os.path.exists(newpath):
    os.makedirs(newpath)
    return "Created {0}.".format(newpath)
  else:
    return "ERROR: {0} already exists.".format(newpath) 

def MKFILE(filename):
  """ Creates a file using a filename or path """
  # FIX ME: WILL NOT CREATE FILE 
  if not os.path.exists(filename):
    f= open(filename,"w+")
    f.close()
    return "Created {0}.".format(filename)
  else:
    return "ERROR: {0} already exists.".format(filename)

def LIST():
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

def PRINT(message):
  """ Print out to the screen a message """
  message = message.split(" ")
  del message[0]
  return " ".join(message)

def MOVE(filename,directory):
  return "Moved: {0} to {1}".format(filename, directory)  

def COPY(filename,new_filename):
  return "Copied: {0} to {1}".format(filename, new_filename)

def ENTER(directory):
  return "Directory: {0}".format(directory)

def MSG(data, index):
  return data.split(" ")[index]

def current_directory():
  return os.path.dirname(os.path.abspath(__file__))  

def check(data):
  """ Checks if the user input command and then calls the command functions """
  command =  data.split(" ")[0]
  command = command.lower()
  path = "/"
  if command == "quit" or command == "exit":
    return QUIT()
  elif command == "print" or command == "echo":
    return PRINT(data)
  elif command == "enter" or command == "cd":
    return ENTER(MSG(data, 1))
  elif command == "list" or command == "ls":
    return LIST()  
  elif command == "mkdir":
    return MKDIR(MSG(data, 1))
  elif command == "mkfile" or command == "touch":
    return MKFILE(MSG(data, 1))
  elif command == "move":
    return MOVE(MSG(data, 1), MSG(data, 2))
  elif command == "copy":
    return COPY(MSG(data, 1), MSG(data, 2))
  else:
    print("ERROR: No such command exist")

if __name__ == '__main__':
  print("Welcome to Python Command Line:")
  while True:
    user_input=raw_input(">")
    print(check(user_input))    
    
