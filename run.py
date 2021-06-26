import argparse
from flask import Flask, Markup, render_template, request, send_file
import os
from movie import Movie
from glob import glob
import urllib.parse
from model import database, FileModel


parser = argparse.ArgumentParser()
parser.add_argument('--folder', '-f', type=str, help="Folder for mp4/mkv files")
args = parser.parse_args()
app = Flask(__name__, static_folder=args.folder)

def setup_database():
    database.create_tables([FileModel])

def main():
    setup_database()
    index_files()
    app.run(host='0.0.0.0', port=3000)

def index_files():
    all_movies = []
    allFiles = []
    walk = [args.folder]
    while walk:
        folder = walk.pop(0) + "/"
        files = os.listdir(folder) # items = folders + files
        for f in files:
            f = folder + f
            (walk if os.path.isdir(f) else allFiles).append(f)
            filename = os.path.basename(f)
            ext = filename[-4:]
            filename = filename[:-4]
            if ext == '.mp4' or ext == '.m4v':
                FileModel.get_or_create(filepath=f, extension=ext)
                all_movies.append(Movie(f, filename))

    return all_movies

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
            print(folder)
            if ext == '.mp4' or ext == '.m4v' or ext == '.vtt':
                print(f)
                all_movies.append(Movie(f, filename))

    return all_movies

@app.route("/")
def index():
    movies = FileModel.select()
    return render_template('index.html', movies_len=len(movies), movies=movies)

@app.route("/play")
def play():
    movie = request.args.get('movie')
    movie = urllib.parse.unquote(movie)
    print(movie)
    vtt = movie[:-4]
    vtt = f'{movie}.vtt'
    query = FileModel.select().where(FileModel.filepath == vtt)
    if query.exists():
        print('Have subs')
    return render_template('play.html', movie=urllib.parse.unquote(movie))

@app.route("/test")
def test():
    return render_template('test.html')

if __name__ == '__main__':
    main()