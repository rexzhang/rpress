#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from datetime import datetime
from sqlalchemy import desc, asc, func, extract

import flask
from flask import request, redirect, url_for, flash, abort
from flask.views import MethodView
from flask.ext.login import login_required

from rpress import db
from rpress.helpers.template import render_template
from rpress.models import Post, User, Term, Comment
from rpress.permission import login_user, logout_user


post = flask.Blueprint('post', __name__)


##class TestView(MethodView):
##    def get(self):
##        return 'hello world'
##
##post.add_url_rule('/test',view_func=TestView.as_view('test'),methods=['GET',])

"""
content = {
    'navigation': {
    },

    'blog_roll': {
        'blog_roll': [
            {
                'title': 'aaaa',
                'author': 'bbbb',
                'date': 'cccc',
                'excerpt': 'dddd',
                'full_link': 'eee',
            },
            {
                'title': 'aaaa222',
                'author': 'bbbb222',
                'date': 'cccc222',
                'excerpt': 'dddd222',
                'link': 'eee222',
            },
        ],
        'prev_page': 'ppppp',
        'next_page': 'nnnnn',
    },
    'post': {

    },
    'widget': {
        'category': [
            {
                'name': 'aaa',
                'desc': 'ccc',
                'link': 'bbb',
            },
            {
            }
        ],

    },
}
"""


#----------------------------------------------------------------------
def _post_roll(posts):
    """internal funtion"""
    post_roll = []
    for post in posts:
        post_roll.append({
            'title': post.title,
            'author': post.creater.name,
            'create_date': post.create_date,
            'excerpt': post.content[:50],
            'link': url_for('post.post_uuid', uuid=post.uuid),
        })

    return post_roll


#----------------------------------------------------------------------
def _sidebar():
    """"""
    categories = []
    terms = Term.query.filter_by(type='category').order_by('name').all()
    for term in terms:
        categories.append({
            'display': term.display,
            'desc': term.name,
            'link': url_for('post.post_term_category', term=term.name),
        })

    tags = []
    terms = Term.query.filter_by(type='tag').order_by('name').all()
    for term in terms:
        tags.append({
            'display': term.display,
            'desc': term.name,
            'link': url_for('post.post_term_tag', term=term.name),
        })

    widgets = {
        'categories': categories,
        'tags': tags,
        'date_years': _widget_date_year(),
    }

    return widgets


#----------------------------------------------------------------------
def _widget_date_year():
    """"""
    date_years = {}

    posts = Post.query.filter_by(type='blog', publish=True).all()
    for post in posts:
        year = post.create_date.year

        if year not in date_years:
            date_years[year] = {
                'display': str(year),
                'link':  url_for('post.post_date', year=year),
                'count': 1,
            }

        date_years[year]['count'] += 1

    return date_years


@post.route('/', methods=['GET'])
#----------------------------------------------------------------------
def index():
    """"""
    posts = Post.query.filter_by(type='blog', publish=True).order_by(desc('create_date')).limit(10)
    post_roll = _post_roll(posts)

    widgets = _sidebar()

    content = {
        'post_roll': post_roll,
        'widgets': widgets,
    }

    return render_template('index.html', content=content)


@post.route('/date/<int:year>', methods=['GET'])
#----------------------------------------------------------------------
def post_date(year):
    """"""
    posts = Post.query.filter_by(type='blog', publish=True) \
        .filter(Post.create_date>=datetime(year, 1, 1),
                Post.create_date<datetime(year+1, 1, 1)).order_by(desc('create_date')).all()
    post_roll = _post_roll(posts)

    widgets = _sidebar()

    content = {
        'post_roll': post_roll,
        'widgets': widgets,
    }

    return render_template('index.html', content=content)


#----------------------------------------------------------------------
def post_term(term):
    """"""
    posts = Post.query.filter_by(type='blog', publish=True).filter(Post.terms.any(Term.name==term)).order_by(desc('create_date')).all()
    #
    post_roll = _post_roll(posts)

    widgets = _sidebar()

    content = {
        'post_roll': post_roll,
        'widgets': widgets,
    }

    return render_template('index.html', content=content)


@post.route('/category/<string:term>', methods=['GET'])
#----------------------------------------------------------------------
def post_term_category(term):
    """"""
    return post_term(term)


@post.route('/tag/<string:term>', methods=['GET'])
#----------------------------------------------------------------------
def post_term_tag(term):
    """"""
    return post_term(term)


@post.route('/author/<string:author>', methods=['GET'])
#----------------------------------------------------------------------
def post_author(author):
    """"""
    posts = Post.query.filter_by(type='blog', publish=True).filter(Post.creater.has(User.name==author)).order_by(desc('create_date')).all()

    post_roll = _post_roll(posts)

    widgets = _sidebar()

    content = {
        'post_roll': post_roll,
        'widgets': widgets,
    }

    return render_template('index.html', content=content)


#----------------------------------------------------------------------
def _render_post(post):
    """render one post"""
    content = {
        'post': {
            'title': post.title,
            'author': post.creater.name,
            'create_date': post.create_date,
            'content': post.content,
        },
    }

    comment_list = []
    comments = Comment.query.filter_by(post=post).order_by(desc('create_date')).all()
    for comment in comments:
        comment_list.append({
            'author_name': comment.author_name,
            'create_date': comment.create_date,
            'content': comment.content,
        })
        print(comment_list)
    content['comments'] = comment_list

    return render_template('post.html', content=content)


# /post/uuid0001
@post.route('/post/<uuid:uuid>', methods=['GET', ])
#----------------------------------------------------------------------
def post_uuid(uuid):
    """"""
    post = Post.query.filter_by(uuid=str(uuid), publish=True).first_or_404()
    return _render_post(post)


@post.route('/<string:name>', methods=['GET', ])
#----------------------------------------------------------------------
def page_name(name):
    """"""
    post = Post.query.filter_by(name=name, publish=True, type='page').first_or_404()

    return _render_post(post)