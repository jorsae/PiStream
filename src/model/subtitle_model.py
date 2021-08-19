from peewee import *
from model import BaseModel, MovieModel

class SubtitleModel(BaseModel):
    subtitle_id = AutoField()
    filepath = TextField()
    extension = TextField()
    srclang = TextField()
    language = TextField()
    movie_id = ForeignKeyField(MovieModel, to_field='movie_id')

    class Meta:
        table_name = 'subtitles'