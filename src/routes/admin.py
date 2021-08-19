from __main__ import app
from flask import request, render_template

import utility

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    output = ''
    if request.method == 'POST':
        update = request.form.get('update')
        if update:
            movies, subs = utility.index_files(app.static_folder)
            output = f'Indexed: {movies} movies, with {subs} subtitles.'
        purge = request.form.get('purge')
        if purge:
            movies, subs = utility.purge_database()
            output = f'Deleted: {movies} movies, with {subs} subtitles.'

    return render_template("admin.html", output=output)

@app.route('/genre', methods=['GET', 'POST'])
def genre():
    return 'genre'