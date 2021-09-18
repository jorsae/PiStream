from peewee import *
from model import BaseModel, MovieModel

class SubtitleModel(BaseModel):
    subtitle_id = AutoField()
    filepath = TextField()
    extension = TextField()
    srclang = TextField()
    language = TextField()
    movie_id = ForeignKeyField(MovieModel, to_field='movie_id', on_delete='CASCADE') # TODO: Make it delete as a cascade effect

    class Meta:
        table_name = 'subtitles'