from peewee import *
from model import BaseModel, MovieModel, GenreModel

class GenreMovieModel(BaseModel):
    genre_movie_id = AutoField()
    movie_id = ForeignKeyField(MovieModel, to_field='movie_id')
    genre_id = ForeignKeyField(GenreModel, to_field='genre_id')
    
    class Meta:
        table_name = 'genremovies'