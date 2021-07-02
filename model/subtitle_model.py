from peewee import *
from model import SubtitleModel

class SubtitleModel(BaseModel):
    subtitle_id = AutoField()
    filepath = TextField()
    extension = TextField()
    file_id = ForeignKeyField(SubtitleModel, to_field='file_id')

    class Meta:
        table_name = 'subtitles'