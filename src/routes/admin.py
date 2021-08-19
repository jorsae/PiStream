from __main__ import app
from flask import request, render_template

import constants
import utility
from model import *

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    output = ''
    if request.method == 'POST':
        update = request.form.get('update')
        if update:
            movies, subs = utility.index_files(constants.STATIC_FOLDER)
            output = f'Indexed: {movies} movies, with {subs} subtitles.'
        purge = request.form.get('purge')
        if purge:
            movies, subs = utility.purge_database()
            output = f'Deleted: {movies} movies, with {subs} subtitles.'

    return render_template("admin.html", output=output)

@app.route('/genre', methods=['GET', 'POST'])
def genre():
    output = ''
    if request.method == 'POST':
        genre = request.form.get('genre')
        if genre:
            genre_id, created = GenreModel.get_or_create(genre=genre)
            if created:
                output = f"Added genre: '{genre}'"
            else:
                output = f"Failed to add genre: '{genre}'"

    return render_template("genre.html", output=output)