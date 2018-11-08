#!/usr/bin/env python
# coding=utf-8


import flask
from flask import request, redirect, url_for, flash, abort
from flask_login import login_required

from rpress.helpers.template.common import render_template
from rpress.runtimes.auth import user_login, user_logout
from rpress.forms import LoginForm

auth = flask.Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
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
            # return redirect(url_for('.index'))

        flash('Logged in successfully.')

        next_location = request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        # if not next_is_valid(next):
        #    return flaskabort(400)
        return redirect(next_location or url_for('rpadmin_dashboard.dashboard'))

    return render_template('/common/login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    user_logout()

    return redirect(url_for('post_page.paginate_with_all'))
