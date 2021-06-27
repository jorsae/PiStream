import argparse
from flask import Flask, Markup, render_template, request, send_file
import os
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
            if ext == '.mp4' or ext == '.m4v' or ext == '.vtt':
                FileModel.get_or_create(filepath=f, filename=filename, extension=ext)

@app.route("/")
def index():
    movies = FileModel.select().where(FileModel.extension != '.vtt')
    print(movies[0])
    print(movies[0].filepath)
    return render_template('index.html', movies_len=len(movies), movies=movies)

@app.route("/play")
def play():
    movie = request.args.get('movie')
    movie = urllib.parse.unquote(movie)
    print(movie)
    vtt = movie[:-4]
    vtt = f'{vtt}.vtt'
    query = FileModel.select().where(FileModel.filepath == vtt)
    if query.exists():
        return render_template('play.html', movie=urllib.parse.unquote(movie), sub=vtt)
    return render_template('play.html', movie=urllib.parse.unquote(movie))

@app.route("/test")
def test():
    return render_template('test.html')

if __name__ == '__main__':
    main()