from peewee import *
import os, re
import logging
from langdetect import detect

from model import *
import query
import constants
import iso639

# Index all files, will add new files to database.
def index_files(start_folder):
    movies = index_movies(start_folder)
    subs = index_subtitles(start_folder)
    return movies, subs

def index_movies(start_folder):
    movies = 0

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
                query = MovieModel.select().where(MovieModel.filepath == f)
                if query.exists():
                    continue
                m, created = MovieModel.get_or_create(filepath=f, filename=filename, extension=ext)
                if created:
                    logging.info(f'Added movie: {f}')
                    movies += 1
    return movies

def index_subtitles(start_folder):
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
            
            if ext in constants.SUBTITLE_FORMATS:
                query = SubtitleModel.select().where(SubtitleModel.filepath == f)
                if query.exists():
                    continue

                try:
                    iso, language = get_language_from_extension(filename)
                    if language is not None:
                        filename = f'{filename[:-3]}'
                    movie = MovieModel.select().where(MovieModel.filename==filename)
                    if len(movie) > 0:
                        if language is None:
                            iso, language = get_language_from_subtitles(f)
                        sub, created = SubtitleModel.get_or_create(filepath=f, extension=ext, movie_id=movie[0].movie_id, srclang=iso, language=language)
                        if created:
                            logging.info(f'Added subtitles: {f}')
                            subs += 1
                except Exception as e:
                    input()
                    logging.error(f'{f}: {e}')
    return subs

# Remove all files in database that has been removed
def ensure_exists():
    deleted_movies = 0
    deleted_subs = 0
    try:
        movies = MovieModel.select()
        for movie in movies:
            if os.path.isfile(movie.filepath) is False:
                # TODO: Make this delete on cascade, so I don't have to fetch id everytime
                deleted_movies += MovieModel.delete().where(MovieModel.movie_id == movie.movie_id).execute()
                deleted_subs += SubtitleModel.delete().where(SubtitleModel.movie_id == movie.movie_id).execute()
                wm = WatchModel.delete().where(WatchModel.movie_id == movie.movie_id).execute()
        # TODO: Do the same for subtitles
        return deleted_movies, deleted_subs
    except Exception as e:
        logging.error(e)
        return None, None

# Delete all tables
def purge_database():
    movies = MovieModel.select(fn.COUNT(MovieModel)).scalar()
    subs = SubtitleModel.select(fn.COUNT(SubtitleModel)).scalar()
    MovieModel.delete().execute()
    SubtitleModel.delete().execute()
    GenreModel.delete().execute()
    GenreMovieModel.delete().execute()
    return movies, subs

# Get all genres for movie, based on movie_id
def get_movie_genres(movie_id):
    genres = GenreMovieModel.select().where(GenreMovieModel.movie_id == movie_id)
    g = []
    for genre in genres:
        gg = GenreModel.select(GenreModel.genre).where(GenreModel.genre_id == genre.genre_id)
        if len(gg) > 0:
            g.append(gg[0].genre)
    return g

# Get all movies with genre:
def get_movies_by_genre(search):
    try:
        genre_id = GenreModel.select(GenreModel.genre_id).where(GenreModel.genre ** search).scalar()
        movies = GenreMovieModel.select(GenreMovieModel.movie_id).where(GenreMovieModel.genre_id == genre_id)
        return MovieModel.select().where(MovieModel.movie_id << movies)
    except Exception as e:
        logging.error(e)
        return []

def get_movies_by_search(searchField, search):
    try:
        return (MovieModel
                .select()
                .where(searchField.contains(search))
                )
    except Exception as e:
        logging.error(e)
        return []

def get_language_from_subtitles(f):
    try:
        data = open(f, 'r', encoding='iso_8859_1').read()
        parsed_data = ''
        for line in data:
            if '-->' not in line:
                parsed_data += line
        iso = detect(data)
        language = iso639.translate[iso]
        return iso, language
    except Exception as e:
        logging.error(e)
        return None, None

def get_language_from_extension(filename):
    iso = None
    language = None
    try:
        iso = filename[-3:]
        if constants.RE_SUBTITLE_EXTENSION.match(iso):
            iso = iso[1:]
            language = iso639.translate[iso]
        return iso, language
    except Exception as e:
        logging.error(e)
        return None, None