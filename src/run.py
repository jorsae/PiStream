import argparse
from flask import Flask, Markup, render_template, request, send_file
import os
from glob import glob
import urllib.parse
import logging

import constants
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
    database.create_tables([MovieModel, GenreModel, SubtitleModel])

def main():
    setup_logging()
    setup_database()
    app.run(host='0.0.0.0', port=3000)

@app.route('/')
def index():
    movies = MovieModel.select().where(MovieModel.extension != '.vtt')
    return render_template('index.html', movies=movies)

@app.route('/play')
def play():
    request_path = request.args.get('movie')
    request_path = urllib.parse.unquote(request_path)
    try:
        movie = MovieModel.select().where(MovieModel.filepath == request_path)
        subtitles = SubtitleModel.select().where(SubtitleModel.movie_id == movie[0].movie_id)
        if len(subtitles) > 0:
            return render_template('play.html', movie=movie[0].filepath, sub=subtitles[0].filepath)
        else:
            return render_template('play.html', movie=movie[0].filepath)
    except Exception as e:
        logging.error(e)
    
if __name__ == '__main__':
    main()