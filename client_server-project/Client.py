#BY: Jonathan Chauwa
import socket
class Client:
    def __init__(self,host,port):
                 self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 self.host = host
                 self.port = port                  
                 self.socket.connect((self.host,self.port))
                                             
    def message(self,message):
                 self.socket.sendall(b,message)
                 data = self.socket.recv(1024)
                 self.socket.close()
                 print("Received", repr(data))

def main():

    ob = Client('',12345)
    ob.message("Complete")

                                             

main()
