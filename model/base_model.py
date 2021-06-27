from peewee import *

database = SqliteDatabase('PiStream.sql')

class BaseModel(Model):
    class Meta:
        database = database