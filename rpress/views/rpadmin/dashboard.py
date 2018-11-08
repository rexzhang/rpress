#!/usr/bin/env python
# coding=utf-8


import flask
from flask import flash
from flask_login import login_required

from rpress.helpers.template.common import render_template


app = flask.Blueprint('rpadmin_dashboard', __name__)


@app.route('/')
@login_required
def dashboard():
    content = {}

    flash('alert demo.')

    return render_template(
        'rpadmin/dashboard.html',
        content=content,
    )
