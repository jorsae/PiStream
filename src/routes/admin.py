from __main__ import app
from flask import request, render_template

@app.route("/admin", methods=["GET", "POST"])
def admin():
    output = ''
    if request.method == "POST":
        reindex = request.form.get('reindex')
        if reindex:
            movies, subs = index_files()
            output = f'Indexed {movies} movies, with {subs} subtitles.'

    return render_template("admin.html", output=output)