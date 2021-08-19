from __main__ import app
from flask import request, render_template

import constants
import utility
from model import *

@app.route('/getgenre', methods=['GET', 'POST'])
def getgenre():
    movie_uuid = request.args.get('uuid')
    print(movie_uuid)
    movie = MovieModel.select().where(MovieModel.uuid == movie_uuid)
    if len(movie) <= 0:
        return []
    genres = GenreMovieModel.select().where(GenreMovieModel.movie_id == movie[0].movie_id)
    g = []
    for genre in genres:
        g.append(GenreModel.select(GenreModel.genre).where(GenreModel.genre_id == genre).scalar())
    return str(g)