from peewee import *
from model import BaseModel, UserModel

class IpModel(BaseModel):
    ip_model_id = AutoField()
    ip = TextField()
    user_id = ForeignKeyField(UserModel, to_field='user_id')

    class Meta:
        table_name = 'ips'