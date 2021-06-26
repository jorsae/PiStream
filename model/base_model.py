from peewee import *

database = SqliteDatabase('PiStream-db.sql')

class BaseModel(Model):
    class Meta:
        database = database