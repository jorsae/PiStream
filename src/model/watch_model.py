from peewee import *
from model import BaseModel, MovieModel, UserModel

class WatchModel(BaseModel):
    watch_id = AutoField()
    movie_id = ForeignKeyField(MovieModel, to_field='movie_id')
    user_id = ForeignKeyField(UserModel, to_field='user_id')
    progress = IntegerField(default=0)

    class Meta:
        table_name = 'watch'