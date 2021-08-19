from peewee import *
from model import BaseModel
import uuid

class MovieModel(BaseModel):
    movie_id = AutoField()
    uuid = TextField(default=uuid.uuid4)
    showname = TextField()
    filepath = TextField()
    filename = TextField()
    extension = TextField()
    
    class Meta:
        table_name = 'movies'