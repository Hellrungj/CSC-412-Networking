from peewee import *
from app.loadConfig import *

cfg = load_config('config/config.yaml')
db = SqliteDatabase(cfg['databases']['dev'])

# Create database connection object
class BaseModel(Model):
  class Meta:
    database = db

class User(BaseModel):
  username = CharField(max_length=80)
  password = TextField()
  email = TextField()
  login = BooleanField(default=False)
    
  def __unicode__(self):       
    return self.username

class Role(BaseModel):
  name = CharField(max_length=80)
  description = TextField()

  def __unicode__(self):
    return self.role

class User_Role(BaseModel):
  user = CharField(max_length=80)
  role = CharField(max_length=80)

  def __unicode__(self):
    return self.username

class MailBox(BaseModel):
  owner = CharField(max_length=80)
  sender = CharField(max_length=80)
  title = TextField()
  message = TextField()  

  def __unicode__(self):
    return self.username
    
