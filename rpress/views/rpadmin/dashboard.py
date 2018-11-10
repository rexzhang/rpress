#!/usr/bin/env python
# coding=utf-8


import flask
# from flask import flash
from flask_login import login_required

from rpress.runtimes.rpadmin.template import render_template, navbar

app = flask.Blueprint('rpadmin_dashboard', __name__)


@app.route('/')
@login_required
@navbar(level1='dashboard')
def dashboard():
    content = {}

    # flash('alert demo.')

    return render_template(
        'rpadmin/dashboard.html',
        content=content,
    )
