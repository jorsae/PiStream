import os
import logging

from model import *

# Purge and index all files anew
def index_files():
    movies = 0
    subs = 0

    MovieModel.delete().execute()
    SubtitleModel.delete().execute()

    allFiles = []
    walk = [args.folder]
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
                MovieModel.get_or_create(filepath=f, showname=filename, filename=filename, extension=ext)
                movies += 1
            elif ext in constants.SUBTITLE_FORMATS:
                try:
                    mm = MovieModel.select().where(MovieModel.filename==filename)
                    if mm is not None:
                        SubtitleModel.get_or_create(filepath=f, extension=ext, movie_id=mm[0].movie_id)
                except Exception as e:
                    logging.error(e)
                subs += 1
    return movies, subs