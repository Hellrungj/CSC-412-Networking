ui = raw_input("")
print("Input: {0}".format(ui))
command = ui.split(" ")[0]
print("Command: {0}".format(command))
message = ui.split(" ")
del message[0]
message = ' '.join(message)
print("Message: {0}".format(message))
