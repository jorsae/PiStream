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
            id = IpModel.select(IpModel.user_id).where(IpModel.ip == ip).scalar()
            if id is None:
                output = 'You are not assigned a username'
            else:
                user = UserModel.select().where(UserModel.user_id == id)[0]
        except Exception as e:
            logging.error(e)
        return render_template("settings.html", user=user, output=output)
    
    username = request.form.get('username')
    if username:
        try:
            user, created = UserModel.get_or_create(username=username)
            
            query = IpModel.select().where(IpModel.ip == ip)
            if query.exists():
                if query[0].user_id != user.user_id:
                    IpModel.update(user_id=user.user_id).where(IpModel.ip == ip).execute()
                    output = f'Updated username to: {username}'
            else:
                ipm, created = IpModel.get_or_create(ip=ip, user_id=user.user_id)
                if created:
                    output = f'Assigned you username: {username}'
                else:
                    output = f'Failed to assign username: {username}'
        except Exception as e:
            logging.error(e)
            output = 'Failed to save settings'

    return render_template("settings.html", user=user, output=output)