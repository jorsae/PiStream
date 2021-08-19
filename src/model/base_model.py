from peewee import *
import constants

database = SqliteDatabase(constants.DATABASE_FILE)

class BaseModel(Model):
    class Meta:
        database = database