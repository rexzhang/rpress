#!/usr/bin/env python
#coding=utf-8


from flask import Blueprint
from flask.views import MethodView
from flask.ext.sqlalchemy import SQLAlchemy

from rpress import helpers
from rpress.models import Post, User


instance = Blueprint('index',__name__)


class TestView(MethodView):
    def get(self):
        return 'hello world'


########################################################################
class BlogView(MethodView):
    """"""
    #----------------------------------------------------------------------
    def get(self, post):
        """"""
        print('post:', post)
        blog = Post.query.filter_by(id=post).first_or_404()

        return helpers.render_template('blog.html', blog=blog)

instance.add_url_rule('/test',view_func=TestView.as_view('test'),methods=['GET',])
instance.add_url_rule('/blog/<int:post>',view_func=BlogView.as_view('blog'),methods=['GET',])
