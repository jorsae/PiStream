from flask import Flask, render_template, request
import argparse
import os
import logging

import constants
import utility
from model import *

parser = argparse.ArgumentParser()
parser.add_argument('--folder', '-f', type=str, default='../Shows', help='Folder for mp4/mkv files')
args = parser.parse_args()
constants.STATIC_FOLDER = args.folder
app = Flask(__name__, static_folder=constants.STATIC_FOLDER)

from routes import *

def setup_logging():
    logFolder = '../logs'
    logFile = 'pistream.log'
    if not os.path.isdir(logFolder):
        os.makedirs(logFolder)
    handler = logging.FileHandler(filename=f'{logFolder}/{logFile}', encoding='utf-8', mode='a+')
    logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d] %(message)s')

def setup_database():
    database.create_tables([MovieModel, GenreModel, SubtitleModel, GenreMovieModel, UserModel, IpModel, WatchModel])

def main():
    setup_logging()
    setup_database()
    app.run(host='0.0.0.0', port=3000)

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
        
        if len(subtitles) > 0:
            return render_template('play.html', movie=movie, sub=subtitles[0], next=next, previous=previous)
        else:
            return render_template('play.html', movie=movie, next=next, previous=previous)
    except Exception as e:
        logging.error(e)
        return render_template('play.html')
    
if __name__ == '__main__':
    main()