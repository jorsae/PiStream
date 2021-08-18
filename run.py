import argparse
from flask import Flask, Markup, render_template, request, send_file
import os
from glob import glob
import urllib.parse

import constants
from model import *


parser = argparse.ArgumentParser()
parser.add_argument('--folder', '-f', type=str, help="Folder for mp4/mkv files")
args = parser.parse_args()
app = Flask(__name__, static_folder=args.folder)

def setup_database():
    database.create_tables([MovieModel, GenreModel, SubtitleModel])

def main():
    setup_database()
    app.run(host='0.0.0.0', port=3000)

def index_files():
    movies = 0
    subs = 0

    MovieModel.delete().execute()

    allFiles = []
    walk = [args.folder]
    while walk:
        folder = walk.pop(0) + "/"
        files = os.listdir(folder) # items = folders + files
        for f in files:
            print(f'{f} | {folder}')
            f = folder + f
            (walk if os.path.isdir(f) else allFiles).append(f)
            filename = os.path.basename(f)
            ext = filename[-4:]
            filename = filename[:-4]
            if ext in constants.VIDEO_FORMATS:
                MovieModel.get_or_create(filepath=f, showname=filename, filename=filename, extension=ext)
                movies += 1
            elif ext in constants.SUBTITLE_FORMATS:
                MovieModel.get_or_create(filepath=f, showname=filename, filename=filename, extension=ext)
                # SubtitleModel.get_or_create()
                subs += 1
    return movies, subs

@app.route("/")
def index():
    movies = MovieModel.select().where(MovieModel.extension != '.vtt')
    print(len(movies))
    return render_template('index.html', movies=movies)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    output = ''
    if request.method == "POST":
        reindex = request.form.get('reindex')
        if reindex:
            movies, subs = index_files()
            output = f'Indexed {movies} movies, with {subs} subtitles.'

    return render_template("admin.html", output=output)

@app.route("/play")
def play():
    # TODO: Get movie details and subtitles from db
    movie = request.args.get('movie')
    movie = urllib.parse.unquote(movie)
    vtt = movie[:-4]
    vtt = f'{vtt}.vtt'
    query = MovieModel.select().where(MovieModel.filepath == vtt)
    if query.exists():
        return render_template('play.html', movie=urllib.parse.unquote(movie), sub=vtt)
    return render_template('play.html', movie=urllib.parse.unquote(movie))

@app.route("/test")
def test():
    return render_template('test.html')

if __name__ == '__main__':
    main()