import argparse
from flask import Flask, Markup, render_template, request
import os
from movie import Movie
from glob import glob
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('--folder', '-f', type=str, help="Folder for mp4/mkv files")
args = parser.parse_args()
print(args.folder)

app = Flask(__name__, static_folder=args.folder)

# os.path.basename(filepath)

def get_movies(root):
    all_movies = []
    allFiles = []
    walk = [root]
    while walk:
        folder = walk.pop(0) + "/"
        files = os.listdir(folder) # items = folders + files
        for f in files:
            f = folder + f
            (walk if os.path.isdir(f) else allFiles).append(f)
            filename = os.path.basename(f)
            ext = filename[-4:]
            if ext == '.mp4' or ext == '.mkv' or ext == '.m4v':
                all_movies.append(Movie(f, filename))

    return all_movies

@app.route("/")
def index():
    movies = get_movies(args.folder)
    print(movies[0].filepath)
    print(len(movies))
    return render_template('index.html', movies_len=len(movies), movies=movies)

@app.route("/play")
def play():
    movie = request.args.get('movie')
    movie = urllib.parse.unquote(movie)
    print(movie)
    movie = f'file://{movie}'
    print(movie)
    # filename = os.path.basename(f)
    # folder = movie.replace(filename, '')
    return render_template('play.html', movie=urllib.parse.unquote(movie))

app.run(host='0.0.0.0', port=3000)