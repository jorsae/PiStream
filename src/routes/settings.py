from __main__ import app
from flask import request, render_template
import logging

import constants
import utility
from model import *

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user = None
    ip = request.remote_addr
    output = ''
    
    if request.method == 'GET':
        try:
            user = UserModel.select().where(UserModel.ip == ip).get()
        except Exception as e:
            logging.error(e)
        return render_template("settings.html", user=user, output=output)
    
    username = request.form.get('username')
    if username:
        try:
            query = UserModel.select().where(UserModel.ip == ip)
            if query.exists():
                UserModel.update(username = username).where(UserModel.ip == ip).execute()
                output = f'Updated username to: {username}'
            else:
                u, created = UserModel.get_or_create(username=username, ip=ip)
                if created:
                    output = f'Created user: {username}'
                else:
                    output = 'Something went wrong'
        except Exception as e:
            logging.error(e)
            output = 'Failed to save settings'

    return render_template("settings.html", user=user, output=output)