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

    'paginate': {
        'title': year,
        'key': year,
        'desc': 'Viewing the date archives',

        'curr_num': page_num,
        'has_prev': post_paginate.has_prev
        'has_next': post_paginate.has_next
        'prev_num': post_paginate.prev_num
        'next_num': post_paginate.next_num

        'view_name': 'post.search',

        'keywords': keywords, #search only

        'posts':[
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
        year = post.publish_date.year

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
    categorys = []
    tags = []
    for term in post.terms:
        if term.type == 'category':
            categorys.append(term.name)
        elif term.type == 'tag':
            tags.append(term.name)

    return {
        'title': post.title,
        'uuid': post.uuid,
        'type': post.type,
        'author': post.author.name,
        'author_id': post.author.id,
        'publish_date': post.publish_date,
        'excerpt': post.content[:50],
        'content': post.content,
        'categorys': categorys,
        'tags': tags,
        'link': url_for('post.post_uuid', uuid=post.uuid),
    }

#----------------------------------------------------------------------
def _render_post_paginate(query, paginate):
    """"""
    post_paginate = query.paginate(paginate['curr_num'], per_page=10)

    paginate['has_prev'] = post_paginate.has_prev
    paginate['has_next'] = post_paginate.has_next
    paginate['prev_num'] = post_paginate.prev_num
    paginate['next_num'] = post_paginate.next_num

    paginate_posts = []
    for post in post_paginate.items:
        paginate_posts.append(_make_post_info(post))
    paginate['posts'] = paginate_posts

    widgets = _sidebar()

    content = {
        'paginate': paginate,
        'widgets': widgets,
    }

    return render_template('post_paginate.html', content=content)


@post.route('/', methods=['GET'])
@post.route('/paginate/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_paginate(page_num=1):
    """"""
    query = Post.query.filter_by(type='blog', publish=True).order_by(desc('publish_date'))
    paginate = {
        'title': 'Home',  #!!!需要改为站点相关信息
        'curr_num': page_num,
        'view_name': 'post.post_paginate',
    }

    return _render_post_paginate(query, paginate)


@post.route('/date/<int:year>', methods=['GET'])
@post.route('/date/<int:year>/paginate/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_date(year, page_num=1):
    """"""
    query = Post.query.filter_by(type='blog', publish=True) \
        .filter(Post.publish_date>=datetime(year, 1, 1), Post.publish_date<datetime(year+1, 1, 1)) \
        .order_by(desc('publish_date'))
    paginate = {
        'title': year,
        'key': year,
        'desc': 'Viewing the date archives',
        'curr_num': page_num,
        'view_name': 'post.post_date',
    }

    return _render_post_paginate(query, paginate)


#----------------------------------------------------------------------
def post_term(term, paginate):
    """"""
    query = Post.query.filter_by(type='blog', publish=True).filter(Post.terms.any(Term.name==term)).order_by(desc('publish_date'))

    paginate['key'] = term
    paginate['title'] = term  #!!!diaplay name?
    return _render_post_paginate(query, paginate)


@post.route('/category/<string:term>', methods=['GET'])
@post.route('/category/<string:term>/paginate/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_term_category(term, page_num=1):
    """"""
    paginate = {
        'desc': 'Viewing the category',
        'curr_num': page_num,
        'view_name': 'post.post_term_category',
    }

    return post_term(term, paginate)


@post.route('/tag/<string:term>', methods=['GET'])
@post.route('/tag/<string:term>/paginate/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_term_tag(term, page_num=1):
    """"""
    paginate = {
        'desc': 'Viewing the tag',
        'curr_num': page_num,
        'view_name': 'post.post_term_tag',
    }

    return post_term(term, paginate)


@post.route('/author/<string:author>', methods=['GET'])
@post.route('/author/<string:author>/paginate/<int:page_num>', methods=['GET'])
#----------------------------------------------------------------------
def post_author(author, page_num=1):
    """"""
    query = Post.query.filter_by(type='blog', publish=True).filter(Post.author.has(User.name==author)).order_by(desc('publish_date'))
    paginate = {
        'title': author,  #!!!display name
        'curr_num': page_num,
        'view_name': 'post.post_author',
    }

    return _render_post_paginate(query, paginate)


@post.route("/search/")
@post.route("/search/paginate/<int:page_num>/")
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

    paginate = {
        'title': keywords,
        'key': keywords,
        'desc': 'Search results for',
        'curr_num': page_num,
        'view_name': 'post.search',

        'keywords': keywords,
    }

    return _render_post_paginate(post_query, paginate)


#----------------------------------------------------------------------
def _render_post(post):
    """render one post"""
    content = {
        'post': _make_post_info(post),
    }

    comment_list = []
    comments = Comment.query.filter_by(post=post).order_by(desc('publish_date')).all()
    for comment in comments:
        comment_list.append({
            'author_name': comment.author_name,
            'publish_date': comment.publish_date,
            'content': comment.content,
        })
        #print(comment_list)
    content['comments'] = comment_list

    return render_template('post.html', content=content)


# /post/uuid0001
@post.route('/post/<uuid:uuid>', methods=['GET', ])
#----------------------------------------------------------------------
def post_uuid(uuid):
    """"""
    post = Post.query.filter_by(uuid=str(uuid), publish=True).first_or_404()
    return _render_post(post)


# /about
@post.route('/<string:name>', methods=['GET', ])
#----------------------------------------------------------------------
def page_name(name):
    """"""
    post = Post.query.filter_by(name=name, publish=True, type='page').first_or_404()
    return _render_post(post)
