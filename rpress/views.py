#!/usr/bin/env python
#coding=utf-8


import flask
from flask import request, redirect, url_for, flash, abort
from flask.views import MethodView
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_required


from rpress import db
from rpress.helpers import render_template
from rpress.models import Post, User
from rpress.forms import PostEditForm, LoginForm
from rpress.permission import login_user, logout_user


post = flask.Blueprint('index',__name__)


class TestView(MethodView):
    def get(self):
        return 'hello world'

post.add_url_rule('/test',view_func=TestView.as_view('test'),methods=['GET',])


@post.route('/', methods=['GET'])
#----------------------------------------------------------------------
def index():
    """"""
    text = 'this is home page'
    return render_template('index.html', text=text)


@post.route('/blog/<int:post_id>', methods=['GET', 'POST'])
#----------------------------------------------------------------------
def blog(post_id):
    """"""
    blog = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('blog.html', blog=blog)


@post.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
def post_edit(post_id):
    """"""
    post = Post.query.filter_by(id=post_id).first_or_404()  #!!!
    form = PostEditForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()

        #flash(_("Posting success"), "success")
        #return redirect(url_for('.blog'))
    else:
        pass

    return render_template("post_edit.html", post_id=post_id, form=form)


@post.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        if not login_user(form.username.data, form.password.data):
            flash('login fail.')
            abort(401)
            #return redirect(url_for('.index'))

        flash('Logged in successfully.')

        next = request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
##        if not next_is_valid(next):
##            return flaskabort(400)

        return redirect(next or url_for('.index'))

    return render_template('login.html', form=form)


@post.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for('.index'))
