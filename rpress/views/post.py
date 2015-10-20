#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from datetime import datetime
from sqlalchemy import desc, asc, func, extract

import flask
from flask import request, redirect, url_for, flash, abort
from flask.views import MethodView

from rpress import db
from rpress.helpers.template.common import render_template
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

    'post_roll': {
        'post_roll': [
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

    'page': {
        'curr_num': page_num,
        'view_name': 'post.search',

        'keywords': keywords, #search only
    }

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


#----------------------------------------------------------------------
def _make_post_info(post):
    """"""
    return {
        'title': post.title,
        'uuid': post.uuid,
        'type': post.type,
        'author': post.creater.name,
        'author_id': post.creater.id,
        'create_date': post.create_date,
        'excerpt': post.content[:50],
        'content': post.content,
        'link': url_for('post.post_uuid', uuid=post.uuid),
    }

#----------------------------------------------------------------------
def _render_post_paginate(query, page):
    """"""
    post_paginate = query.paginate(page['curr_num'], per_page=10)

    post_roll = []
    for post in post_paginate.items:
        post_roll.append(_make_post_info(post))

    page['has_prev'] = post_paginate.has_prev
    page['has_next'] = post_paginate.has_next
    page['prev_num'] = post_paginate.prev_num
    page['next_num'] = post_paginate.next_num

    widgets = _sidebar()

    content = {
        'post_roll': post_roll,
        'page': page,
        'widgets': widgets,
    }

    return render_template('post_paginate.html', content=content)


@post.route('/', methods=['GET'])
@post.route('/page/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_page(page_num=1):
    """"""
    query = Post.query.filter_by(type='blog', publish=True).order_by(desc('create_date'))
    page = {
        'title': 'Home',  #!!!需要改为站点相关信息
        'curr_num': page_num,
        'view_name': 'post.post_page',
    }

    return _render_post_paginate(query, page)


@post.route('/date/<int:year>', methods=['GET'])
@post.route('/date/<int:year>/page/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_date(year, page_num=1):
    """"""
    query = Post.query.filter_by(type='blog', publish=True) \
        .filter(Post.create_date>=datetime(year, 1, 1), Post.create_date<datetime(year+1, 1, 1)) \
        .order_by(desc('create_date'))
    page = {
        'title': year,
        'key': year,
        'desc': 'Viewing the date archives',
        'curr_num': page_num,
        'view_name': 'post.post_date',
    }

    return _render_post_paginate(query, page)


#----------------------------------------------------------------------
def post_term(term, page):
    """"""
    query = Post.query.filter_by(type='blog', publish=True).filter(Post.terms.any(Term.name==term)).order_by(desc('create_date'))

    page['title'] = term  #!!!diaplay name?
    return _render_post_paginate(query, page)


@post.route('/category/<string:term>', methods=['GET'])
@post.route('/category/<string:term>/page/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_term_category(term, page_num=1):
    """"""
    page = {
        'key': term,
        'desc': 'Viewing the category',
        'curr_num': page_num,
        'view_name': 'post.post_term_category',
    }

    return post_term(term, page)


@post.route('/tag/<string:term>', methods=['GET'])
@post.route('/tag/<string:term>/page/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_term_tag(term, page_num=1):
    """"""
    page = {
        'key': term,
        'desc': 'Viewing the tag',
        'curr_num': page_num,
        'view_name': 'post.post_term_tag',
    }

    return post_term(term, page)


@post.route('/author/<string:author>', methods=['GET'])
@post.route('/author/<string:author>/page/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_author(author, page_num=1):
    """"""
    query = Post.query.filter_by(type='blog', publish=True).filter(Post.creater.has(User.name==author)).order_by(desc('create_date'))
    page = {
        'title': author,  #!!!display name
        'curr_num': page_num,
        'view_name': 'post.post_author',
    }

    return _render_post_paginate(query, page)


@post.route("/search/")
@post.route("/search/page/<int:page_num>/")
#----------------------------------------------------------------------
def search(page_num=1):
    """"""
    keywords = request.args.get('keywords', '').strip(',')

    if not keywords:
        return redirect(url_for("post.index"))

    post_query = Post.query.search(keywords)  #!!!!当前搜索多个关键字有bug

    if post_query.count() == 1:
        #only one result
        posts = post_query.all()
        post = posts[0]
        return redirect(url_for('post.post_uuid', uuid=post.uuid))

    page = {
        'title': keywords,
        'key': keywords,
        'desc': 'Search results for',
        'curr_num': page_num,
        'view_name': 'post.search',

        'keywords': keywords,
    }

    return _render_post_paginate(post_query, page)


#----------------------------------------------------------------------
def _render_post(post):
    """render one post"""
    content = {
        'post': _make_post_info(post),
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
