import datetime

class Logging():
  def __init__(self, filename):
    self.filename = filename
    self.file = None

  def log_time(self):
    local_time = datetime.datetime.now()
    return(local_time.strftime("%m-%d-%Y %H:%M:%S"))

  def start_log(self):
    # Add a statement thaa looks for log file
    self.file = open(self.filename, "w")
    print("{1} Created {0}".format(self.filename, self.log_time()))

  def end_log(self):
    print("{1} Closing {0}".format(self.filename, self.log_time()))
    self.file.close()
