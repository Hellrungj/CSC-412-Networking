#Name: John Hellrung
import glob
import os
import sys

def GLOB(path):
  os.chdir(path)
  for file in glob.glob("*.txt"):
    print(file)

def LISTDIR(path):
  for file in os.listdir(path):
      if file.endswith(".txt"):
          print(os.path.join("/", file))

def WALK(path):   
  #for root, dirs, files in os.walk(path):
      #for file in files:
          #if file.endswith(".py"):
             #print(os.path.join(root, file))
  for files in os.walk(path):
    files = files[2]
    S_files = sorted(files, key=str.lower)
    for file in S_files:
      sys.stdout.write("{0} ".format(file))
    print("")
  

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print ("Usage: ")
    print (" python testing2.py <method>")
    print (" e.g. python testing2.py GLOB")
    print
    sys.exit()
  method = sys.argv[1]
  path = os.path.dirname(os.path.abspath(__file__))
  if method.lower() == 'glob':
    GLOB(path)
  elif method.lower() == 'listdir':
    LISTDIR(path)
  elif method.lower() == 'walk':
    WALK(path)
  else:
    print('ERROR')
    
