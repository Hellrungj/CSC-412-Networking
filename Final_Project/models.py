from peewee import *
from flask_peewee.db import Database
from flask_security import UserMixin, RoleMixin

import os
#from allImports import *   #Don't believe this import is needed for this file
# Create a database
from loadConfig import *

cfg = load_config('config.yaml')
db = SqliteDatabase(cfg['databases']['dev'])

# Create database connection object
class BaseModel(Model):
  class Meta:
    database = db

class UD(BaseModel, UserMixin):
  username = CharField(max_length=80)
  password = TextField()
  login = BooleanField(default=False)
    
  def __unicode__(self):       
    return self.username

class MBX(BaseModel):
  username = CharField(max_length=80)
  message = TextField()

  def __unicode__(self):
    return self.username
    
