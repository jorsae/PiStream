from peewee import *
from model import BaseModel

class MovieModel(BaseModel):
    file_id = AutoField()
    showname = TextField()
    filepath = TextField()
    filename = TextField()
    extension = TextField()
    
    class Meta:
        table_name = 'files'