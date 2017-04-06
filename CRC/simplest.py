import sys

def file_data(filename):
  f = open(filename, "r")
  return f

def CRC(data):
  total = 0
  for line in data:
    for ch in line:
      #print(ch)
      if not ch in " ":
        total += ord(ch) 
  return total

def modulo(data):
  return CRC(data) % 13

def moduli(data):
  return CRC(data) % 17

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print ("Usage: ")
    print (" python simplest <filename>")
    print (" e.g. python simplest text.txt")
    print
    sys.exit()
  filename = sys.argv[1]
 
  print("CRC Number: {0}".format(CRC(file_data(filename))))
  print("Modulo Number: {0}".format(modulo(file_data(filename))))
  print("Moduli Number: {0}".format(moduli(file_data(filename))))
