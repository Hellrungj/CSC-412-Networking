# BY: John Hellrung
import socket

class Server():
	def __init__ (self, server_address):
		self.host, self.port = server_address
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def run(self):
		self.socket.bind((self.host, self.port))
		self.socket.listen(1)
		conn, addr = self.socket.accept()
		print("Connect by", addr)
		while True:
			data = conn.recv(1024)
			if not data: break
			conn.sendall(data)
		conn.close()

def main():
        S = Server(("",12345))
        S.run()

main()
