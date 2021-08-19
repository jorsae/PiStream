from __main__ import app
from flask import request, render_template

import constants
import utility
from model import *

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    output = ''
    if request.method == 'POST':
        update = request.form.get('update')
        if update:
            movies, subs = utility.index_files(constants.STATIC_FOLDER)
            output = f'Indexed: {movies} movies, with {subs} subtitles.'
        purge = request.form.get('purge')
        if purge:
            movies, subs = utility.purge_database()
            output = f'Deleted: {movies} movies, with {subs} subtitles.'

    return render_template("admin.html", output=output)

@app.route('/genre', methods=['GET', 'POST'])
def genre():
    UiMovies = []
    movies = MovieModel.select().where(MovieModel.extension != '.vtt')
    for movie in movies:
        genres = utility.get_movie_genres(movie.movie_id)
        if len(genres) > 0:
            print(genres)
        UiMovies.append(UiMovie(movie.filename, movie.uuid, str(genres)))
    
    genres = GenreModel.select()

    output = ''
    if request.method == 'POST':
        if request.form.get('movie_uuid'):
            genre_id = request.form.get('genre_id')
            movie_uuid = request.form.get('movie_uuid')
            
            movie = MovieModel.select().where(MovieModel.uuid == movie_uuid)
            genre = GenreModel.select().where(GenreModel.genre_id == genre_id)
            if len(movie) > 0 and len(genre) > 0:
                gm, created = GenreMovieModel.get_or_create(movie_id=movie[0].movie_id, genre_id=genre[0].genre_id)
                if created:
                    output = 'Added genre to movie'
            else:
                output = 'Failed to add genre to movie'
        else:
            genre = request.form.get('genre')
            if genre:
                genre_id, created = GenreModel.get_or_create(genre=genre)
                if created:
                    output = f"Added genre: '{genre}'"
                else:
                    output = f"Failed to add genre: '{genre}'"

    return render_template("genre.html", output=output, movies=UiMovies, genres=genres)