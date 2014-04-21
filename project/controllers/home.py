# -*- coding: utf-8 -*-
from project import app, security
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators


class CreateForm(Form):
    text = TextField(u'Text:', [validators.Length(min=1, max=200)])


@app.route('/')
@security()
def start(user=None):
    return render_template('home/home.html',user=user)

@app.route('/print', methods=['GET', 'POST'])
def printer():
    form = CreateForm(request.form)
    return render_template('printer/index.html')
    # return render_template('printer/print.html', form=form)

@app.route('/test', methods=['GET', 'POST'])
def model():
    from project.models.User import User
    from project.models.Library import Library
    from project.models.Movie import Movie
    User.objects().delete()
    Library.objects().delete()
    Movie.objects().delete()
    
    user = User(email='test@test.com', password='password').save()
    testCollection = Library( user=user, unit='Movie', name='Action').save()
    movie = Movie(title="SpiderMan",summary="SpiderMan gets the girl and saves the day").save()
    movie.addTag('action').save()
    user.addRole('kangaroo').save()
    testCollection.addUnit(movie).save()
    m = testCollection.getUnit(0)
    return render_template('printer/index.html')
