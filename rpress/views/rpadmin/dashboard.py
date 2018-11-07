#!/usr/bin/env python
# coding=utf-8


import flask
from flask import Blueprint, redirect, url_for, flash
# from flask import render_template, request
from flask_login import login_required

from rpress.helpers.template.common import render_template


app = flask.Blueprint('dashboard', __name__)


@app.route('/')
@login_required
def dashboard():
    content = {}

    print('11111111')
    flash('password is changed!')

    return render_template(
        'rpadmin/dashboard.html',
        content=content,
    )
