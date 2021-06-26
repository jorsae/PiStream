from peewee import *
from model import BaseModel

class FileModel(BaseModel):
    file_id = AutoField()
    filepath = TextField()
    extension = TextField()
    
    class Meta:
        table_name = 'files'