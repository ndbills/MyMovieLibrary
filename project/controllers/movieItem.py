# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators



@app.route('/movie')
def movie():
    return render_template('movieItem/movieItem.html')
