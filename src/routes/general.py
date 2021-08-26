from __main__ import app
from flask import request, render_template, jsonify

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
            return render_template('play.html', movie=movie, sub=subtitles[0], watch_progress=watch_progress, next=next, previous=previous)
        else:
            return render_template('play.html', movie=movie, watch_progress=watch_progress, next=next, previous=previous)
    except Exception as e:
        logging.error(e)
        return render_template('play.html')

@app.route('/watching', methods=['GET', 'POST'])
def watching():
    return 'watching'