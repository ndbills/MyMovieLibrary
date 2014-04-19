# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators


class CreateForm(Form):
    text = TextField(u'Text:', [validators.Length(min=1, max=200)])


@app.route('/')
def start():
    return render_template('home/home.html')

@app.route('/print', methods=['GET', 'POST'])
def printer():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        from app.models.Printer import Printer
        printer = Printer()
        printer.show_string(form.text.data)
        return render_template('home/index.html')
    return render_template('home/print.html', form=form)
