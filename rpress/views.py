#!/usr/bin/env python
#coding=utf-8


from flask import Blueprint
from flask.views import MethodView
from flask.ext.sqlalchemy import SQLAlchemy

from rpress.models import Blog, User

instance = Blueprint('index',__name__)


class TestView(MethodView):
    def get(self):
        return 'hello world'


########################################################################
class BlogView(MethodView):
    """"""
    #----------------------------------------------------------------------
    def get(self):
        """"""
        blog = Blog.query.filter_by(id=1).first_or_404()
        print blog

        return blog.title + blog.content


instance.add_url_rule('/test',view_func=TestView.as_view('test'),methods=['GET',])
instance.add_url_rule('/blog/1',view_func=BlogView.as_view('blog'),methods=['GET',])
