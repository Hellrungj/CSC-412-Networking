import hashlib

class Checksum():
  def __init__(self, msg):
    self.msg = msg

  def md5(self, msg):
    m = hashlib.md5()
    m.update(msg)
    return m.hexdigest()

  def decode_md5(self, msg):
    return hashlib.md5(msg).hexdigest()

  def checksum(self):
    #print("ORG MSG: {0}".format(self.msg))
    msg_splited = self.msg.split(" ")
    chuck = msg_splited[0]
    #print("CHUCKG: {0}".format(chuck))
    del msg_splited[0]
    rest_of_msg = " ".join(msg_splited)
    #print("rest of MSG: {0}".format(rest_of_msg))
    #print("DECODE MSG: {0}".format(self.decode_md5(rest_of_msg)))
    if chuck == self.decode_md5(rest_of_msg):
      return True
    else:
      return False
