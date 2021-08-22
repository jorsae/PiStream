from __main__ import app
from flask import request, render_template

import constants
import utility
from model import *

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template("settings.html")