import sys

global UserData
UserData = {}

def Add_User(name, password):
  UserData[name] = password
  return("User Added")

def Display_Password(username):
  return(UserData[username])

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print ("Usage:")
    print (" python Testing.py <username> <password>")
    print (" For example:")
    print (" python Testing.py hellrungj Natioh22")
    print
    sys.exit()
  USERNAME = sys.argv[1]
  PASSWORD = sys.argv[2]

print(Add_User(USERNAME, PASSWORD))
print(Display_Password(USERNAME))
if UserData.get("John") == None:
  print("Invaild User")  
#print(UserData["John"])
else:
  print("Error")

