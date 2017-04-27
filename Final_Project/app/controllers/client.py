# Messaging Client
import socket
import sys
import hashlib #For the checksum
<<<<<<< HEAD
from interpreter import Interpreter
from checksum import Checksum
from logging import Logging
=======
#from INTERPRETER import Interpreter
#from CHECKSUM import Checksum
#from LOGGING import Logging
>>>>>>> 1e28f59d2b23bed4cafd9290d50aea3e8541a7de

MSGLEN = 1

class Client():
  def __init__(self, host, port):
    self.server_address = (host, port)
    self.Log = Logging("client_log.txt")
    self.Current_Users = []

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

  def Test(self, filename):
    f = open(filename, "r")
    file = f.readlines()
    Counter = 0
    while True:
      line = file[Counter]
      if "EOF" in line:
        break  
      else:      
        command = line.split("\n")[0]     
        self.Log.file.write("{0} MSG: {1}\n".format(self.Log.log_time(),command))
        print(">MSG: {0}".format(command))
        self.send_recv(command)
      Counter += 1

  def send(self, msg):
    check = Checksum(msg)
    #print("MSG: {0}".format(msg))
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect(self.server_address)
    msg = "{1} {0}".format(msg,check.md5(msg)) #Checksum
    length = self.socket.send(bytes(msg + "\0"))
    #print ("SENT MSG: '{0}'".format(msg))
    #print ("CHARACTERS SENT: [{0}]".format(length))

  def recv(self):
    response = self.receive_message()
    #print("ORGIANAL RESPONSE: {0}".format(response))
    check = Checksum(response)
    if not check.checksum():
      response = ("ERROR","Data failed to transfer.")
    #print("RESPONSE: [{0}]".format(response))
    new_response = response.split(" ")
    print(" ".join(new_response[2:]))
    self.Log.file.write("{0} MSG: {1}\n".format(self.Log.log_time(),response))
    self.socket.close()
    return response

  def send_recv (self,msg):
    self.send(msg)
    response = self.recv()
    self.resend(response, msg)

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

  def start_client(self):
    self.Log.start_log()
    self.Log.file.write("{0} Client started\n".format(self.Log.log_time()))
    self.send("CONNECT")    
    
  def interpret(self, data):
    #print("INTERPRETING")   
    run = Interpreter(data)
    msg = run.check()
    if msg in "EXIT":
      self.Log.file.write("{0} Client ended\n".format(self.Log.log_time()))
      self.Log.end_log()
      sys.exit()
    else:
      self.Log.file.write("{0} MSG: {1}\n".format(self.Log.log_time(),msg))
      return msg 


