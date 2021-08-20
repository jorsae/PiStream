from flask import Flask, render_template, request, jsonify
from glob import glob
import argparse
import os
import json
import urllib.parse
import logging

import constants
import utility
from model import *

parser = argparse.ArgumentParser()
parser.add_argument('--folder', '-f', type=str, default='../Shows', help='Folder for mp4/mkv files')
args = parser.parse_args()
constants.STATIC_FOLDER = args.folder
app = Flask(__name__, static_folder=constants.STATIC_FOLDER)

from routes import admin

def setup_logging():
    logFolder = '../logs'
    logFile = 'pistream.log'
    if not os.path.isdir(logFolder):
        os.makedirs(logFolder)
    handler = logging.FileHandler(filename=f'{logFolder}/{logFile}', encoding='utf-8', mode='a+')
    logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d] %(message)s')

def setup_database():
    database.create_tables([MovieModel, GenreModel, SubtitleModel, GenreMovieModel])

def main():
    setup_logging()
    setup_database()
    app.run(host='0.0.0.0', port=3000)

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

@app.route('/play')
def play():
    uuid = request.args.get('v')
    try:
        movie = MovieModel.select().where(MovieModel.uuid == uuid)
        subtitles = SubtitleModel.select().where(SubtitleModel.movie_id == movie[0].movie_id)

        next = MovieModel.select().where(MovieModel.movie_id == (movie[0].movie_id + 1))
        if len(next) > 0:
            next = next[0]
        else:
            next = None
        previous = MovieModel.select().where(MovieModel.movie_id == (movie[0].movie_id -1))
        if len(previous) > 0:
            previous = previous[0]
        else:
            previous = None

        if len(subtitles) > 0:
            return render_template('play.html', movie=movie[0].filepath, sub=subtitles[0], next=next, previous=previous)
        else:
            return render_template('play.html', movie=movie[0].filepath, next=next, previous=previous)
    except Exception as e:
        logging.error(e)
    
if __name__ == '__main__':
    main()