# BY: John Hellrung and Jonathan Chauwa
import socket

class Server():
        def __init__ (self, server_address):
                self.host, self.port = server_address
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.filename = "Log.txt"
                self.file = None           	

        def run(self):
                self.socket.bind((self.host, self.port))
                self.socket.listen(1)
                conn, addr = self.socket.accept()
                print("Connect by", addr)
                self.file.write("Connect by " + str(addr))
                while True:
                        data = conn.recv(1024)
                        if not data: break
                        conn.sendall(data)
                conn.close()
        
	def store(self, filename):
		self.filename = filename
                self.file = open(self.filename, "w+")
		print("Created " + str(self.filename))
		self.run()
		self.file.close()  
			


import socket
class Client():
    def __init__(self,host,port):
                 self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 self.host = host
                 self.port = port
                 self.socket.connect((self.host,self.port))
    def message(self,message):
                 self.socket.sendall(b'message')
                 data = self.socket.recv(1024)
                 self.socket.close()
                 print("Received", repr(data))
