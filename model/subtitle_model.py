from peewee import *
from model import BaseModel, MovieModel

class SubtitleModel(BaseModel):
    subtitle_id = AutoField()
    filepath = TextField()
    extension = TextField()
    file_id = ForeignKeyField(MovieModel, to_field='file_id')

    class Meta:
        table_name = 'subtitles'