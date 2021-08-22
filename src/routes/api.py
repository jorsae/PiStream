from __main__ import app
from flask import request, render_template, jsonify

import constants
import utility
from model import *

@app.route('/', defaults={'page': 1})
@app.route('/<int:page>')
def index(page):
    movies = (MovieModel
                .select()
                .paginate(page, constants.MAX_VIDEO_RESULTS)
            )
    UiMovies = []
    for movie in movies:
        genres = utility.get_movie_genres(movie.movie_id)
        UiMovies.append(UiMovie(movie.filename, movie.uuid, str(genres)))
    
    return render_template('index.html', movies=UiMovies)

@app.route('/search', methods=['GET'])
def search():
    search = request.args.get('search')
    query = (MovieModel
                .select()
                .where(MovieModel.showname.contains(search))
            )

    ui_movies = []
    for m in query:
        ui_movies.append(UiMovie(m.filename, m.uuid, None))
    return jsonify([m.__dict__ for m in ui_movies])

@app.route('/watch', methods=['GET', 'POST'])
def watch():
    return 'watch'
