# Code Snippet 2: Client
import rpyc

# Grab a connection to the server
client = rpyc.connect("localhost", 18861)

# The "root" is the class we registered with the server.
# So, all exposed methods can be called off of the "root".
response = client.root.say_hello()
# If we print the response, it should be "Hello, World!"
print(response)
