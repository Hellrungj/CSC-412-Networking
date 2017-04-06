# Code Snippet 1: Server
import rpyc

class HelloWorldServer(rpyc.Service):
  def on_connect(self):
    pass
  def on_disconnect(self):
    pass
  
  def exposed_say_hello(self):
    return "Hello, World!"

# Launch the server
if __name__ == "__main__":
  from rpyc.utils.server import ThreadedServer
  t = ThreadedServer(HelloWorldServer, port = 18861)
  print("Launching the Server")
  t.start()
