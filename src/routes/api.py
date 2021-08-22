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

@app.route('/watch', methods=['POST'])
def watch():
    ip = request.remote_addr
    json = request.json
    movie_uuid = json['m']
    progress = json['p']
    total_time = json['t']

    user_id = IpModel.select(IpModel.user_id).where(IpModel.ip == ip).scalar()
    if user_id is None:
        print('No assigned username, not tracking watch progress')
        return '', 400
    movie_id = MovieModel.select(MovieModel.movie_id).where(MovieModel.uuid == movie_uuid).scalar()
    if movie_id is None:
        print(f'Could not find movie with uuid: {movie_uuid}')
        return '', 400
    
    wm = (WatchModel
            .select(WatchModel.watch_id)
            .where(
                (WatchModel.movie_id == movie_id) &
                (WatchModel.user_id == user_id)
            )
        ).scalar()
    
    if (total_time - progress) < constants.WATCH_PROGRESS_TIME_EDGE:
        WatchModel.delete().where(WatchModel.watch_id == wm).execute()
        return ''
    
    if progress < constants.WATCH_PROGRESS_TIME_EDGE:
        return ''

    if wm is not None:
        wm = WatchModel.replace(watch_id=wm, movie_id=movie_id, user_id=user_id, progress=progress).execute()
    else:
        wm = WatchModel.replace(movie_id=movie_id, user_id=user_id, progress=progress).execute()
    
    return ''