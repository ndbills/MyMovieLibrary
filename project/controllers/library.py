# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask.ext.wtf import Form, TextField, validators


@app.route('/libraries')
def libraries():
	return render_template('library/master.html')

@app.route('/libraries/<libraryName>')
def library(libraryName):
    return render_template('library/library.html')

@app.route('/libraries/<libraryName>/<int:movieLibraryIndex>')
def libraryItem(libraryName, movieLibraryIndex):
    return render_template('library/libraryItem.html')
