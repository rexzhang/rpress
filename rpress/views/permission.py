#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import flask
from flask import request, redirect, url_for, flash, abort
from flask_login import login_required

from rpress.helpers.template.common import render_template
from rpress.permission import user_login, user_logout
from rpress.forms import LoginForm


permission = flask.Blueprint('permission', __name__)


@permission.route('/login', methods=['GET', 'POST'])
#----------------------------------------------------------------------
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        if not user_login(form.username.data, form.password.data):
            flash('login fail.')
            abort(401)
            #return redirect(url_for('.index'))

        flash('Logged in successfully.')

        next = request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
##        if not next_is_valid(next):
##            return flaskabort(400)
        return redirect(next or url_for('site_admin.index'))

    return render_template('/common/login.html', form=form)


@permission.route("/logout")
@login_required
#----------------------------------------------------------------------
def logout():
    user_logout()

    return redirect(url_for('post.post_paginate'))  #!!!!
