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
    # TODO: Programmatically fetch all classes that inherit BaseModel
    # models = peewee.Model.__subclasses__()
    # print(type(models))
    # for model in models:
    #     print(model)
    database.create_tables([MovieModel, GenreModel, SubtitleModel, GenreMovieModel, UserModel, IpModel, WatchModel])

def main():
    setup_logging()
    setup_database()
    app.run(host='0.0.0.0', port=3000)

if __name__ == '__main__':
    main()