from peewee import *
from model import BaseModel

class GenreModel(BaseModel):
    genre_id = AutoField()
    genre = TextField()
    
    class Meta:
        table_name = 'genres'