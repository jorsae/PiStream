from __main__ import app
from flask import request, render_template, jsonify
import logging

import constants
import utility
from model import *

@app.route('/play')
def play():
    ip = request.remote_addr
    uuid = request.args.get('v')
    try:
        movie = MovieModel.select().where(MovieModel.uuid == uuid)[0]
        subtitles = SubtitleModel.select().where(SubtitleModel.movie_id == movie.movie_id)
        print(len(subtitles))

        next = MovieModel.select().where(MovieModel.movie_id == (movie.movie_id + 1))
        if len(next) > 0:
            next = next[0]
        else:
            next = None
        previous = MovieModel.select().where(MovieModel.movie_id == (movie.movie_id -1))
        if len(previous) > 0:
            previous = previous[0]
        else:
            previous = None
        
        watch_progress = 0
        user_id = IpModel.select(IpModel.user_id).where(IpModel.ip == ip).scalar()
        if user_id is not None:
            watch_progress = (WatchModel
                                .select(WatchModel.progress)
                                .where(
                                    (WatchModel.movie_id == movie.movie_id) &
                                    (WatchModel.user_id == user_id)
                                )
                            ).scalar()

        if len(subtitles) > 0:
            return render_template('play.html', movie=movie, subtitles=subtitles, watch_progress=watch_progress, next=next, previous=previous)
        else:
            return render_template('play.html', movie=movie, watch_progress=watch_progress, next=next, previous=previous)
    except Exception as e:
        logging.error(e)
        return render_template('play.html')

@app.route('/watching', methods=['GET', 'POST'])
def watching():
    ip = request.remote_addr
    try:
        # << 	x IN y, where y is a list or query
        user_id = IpModel.select(IpModel.user_id).where(IpModel.ip == ip).scalar()
        watching = WatchModel.select(WatchModel.movie_id).where(WatchModel.user_id == user_id)
        movies = MovieModel.select().where(MovieModel.movie_id << watching)
        UiMovies = []
        for movie in movies:
            UiMovies.append(UiMovie(movie.filename, movie.uuid, None))
        return render_template('watching.html', movies=movies)
    except Exception as e:
        logging.error(e)

    return render_template('watching.html')
