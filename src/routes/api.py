from __main__ import app
from flask import request, render_template, jsonify
import logging
import time

import constants
import utility
from model import *

@app.route('/')
def index():
    movies = MovieModel.select()
    return render_template('index.html', movies=movies)

@app.route('/search', methods=['GET'])
def search():
    search = request.args.get('search')
    searchType = request.args.get('searchType')

    movies = []
    if searchType == 'path':
        movies = utility.get_movies_by_search(MovieModel.filepath, search)
    elif searchType == 'genre':
        movies = utility.get_movies_by_genre(search)
    else:
        movies = utility.get_movies_by_search(MovieModel.filename, search)
    
    ui_movies = []
    for m in movies:
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

@app.route('/clearwatch', methods=['POST'])
def clearwatch():
    ip = request.remote_addr
    json = request.json
    movie_uuid = json['m']
    try:
        user_id = IpModel.select(IpModel.user_id).where(IpModel.ip == ip).scalar()
        movie_id = MovieModel.select(MovieModel.movie_id).where(MovieModel.uuid == movie_uuid).scalar()
        (WatchModel
            .delete()
            .where(
                (WatchModel.user_id == user_id) &
                (WatchModel.movie_id == movie_id)
                )
            .execute()
        )
        return movie_uuid
    except Exception as e:
        logging.error(e)
        return '', 500