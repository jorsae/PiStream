from peewee import *
from model import BaseModel

class MovieModel(BaseModel):
    movie_id = AutoField()
    uuid = TextField()
    showname = TextField()
    filepath = TextField()
    filename = TextField()
    extension = TextField()
    
    class Meta:
        table_name = 'movies'