from peewee import *
import os
import logging

from model import *
import query
import constants

# Index all files, will add new files to database.
def index_files(start_folder):
    movies = 0
    subs = 0

    allFiles = []
    walk = [start_folder]
    while walk:
        folder = walk.pop(0) + "/"
        files = os.listdir(folder) # items = folders + files
        for f in files:
            f = folder + f
            (walk if os.path.isdir(f) else allFiles).append(f)
            filename = os.path.basename(f)
            ext = filename[-4:]
            filename = filename[:-4]
            
            if ext in constants.VIDEO_FORMATS:
                m, created = MovieModel.get_or_create(filepath=f, showname=filename, filename=filename, extension=ext)
                if created:
                    movies += 1
            elif ext in constants.SUBTITLE_FORMATS:
                try:
                    mm = MovieModel.select().where(MovieModel.filename==filename)
                    if mm is not None:
                        sub, created = SubtitleModel.get_or_create(filepath=f, extension=ext, movie_id=mm[0].movie_id)
                        if created:
                            subs += 1
                except Exception as e:
                    logging.error(e)
    return movies, subs

def purge_database():
    movies = MovieModel.select(fn.COUNT(MovieModel)).scalar()
    subs = SubtitleModel.select(fn.COUNT(SubtitleModel)).scalar()
    MovieModel.delete().execute()
    SubtitleModel.delete().execute()
    return movies, subs