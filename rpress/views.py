#!/usr/bin/env python
#coding=utf-8


from flask import Blueprint, redirect, url_for
from flask.views import MethodView
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, validators, SubmitField

from rpress.database import db
from rpress.helpers import render_template
from rpress.models import Post, User


post = Blueprint('index',__name__)


class TestView(MethodView):
    def get(self):
        return 'hello world'

post.add_url_rule('/test',view_func=TestView.as_view('test'),methods=['GET',])


@post.route('/', methods=['GET'])
#----------------------------------------------------------------------
def test_page():
    """"""
    return 'this is test page'


@post.route('/blog/<int:post_id>', methods=['GET', 'POST'])
#----------------------------------------------------------------------
def blog(post_id):
    """"""
    blog = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('blog.html', blog=blog)


class PostEditForm(Form):
    title = StringField(u'标题', [validators.Length(min=4)])
    content = StringField(u'正文', [validators.Length(min=4)])
    submit = SubmitField("submit")


@post.route('/post/<int:post_id>', methods=['GET', 'POST'])
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
        #return redirect(url_for('blog'))

    return render_template("post_edit.html", post_id=post_id, form=form)

