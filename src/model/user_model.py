from peewee import *
from model import BaseModel

class UserModel(BaseModel):
    user_id = AutoField()
    username = TextField()

    class Meta:
        table_name = 'users'