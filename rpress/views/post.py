#!/usr/bin/env python
# coding=utf-8


from datetime import datetime
from sqlalchemy import desc

import flask
from flask import request, redirect, url_for

from rpress.constants import POST
from rpress.runtimes.template import render_template
from rpress.helpers.mulit_site import get_current_request_site
from rpress.models import Post, User, Term, Comment

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

        'view_name': 'post_page.paginate_with_all',

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

post_page = flask.Blueprint('post_page', __name__)


def _sidebar():
    """"""
    site = get_current_request_site()  # TODO!!!应该传进来

    categories = []
    terms = Term.query.filter_by(site=site, type='category').order_by('name').all()
    for term in terms:
        categories.append({
            'name': term.name,
            'desc': term.desc,
            'link': url_for('post_page.paginate_with_term_category', term=term.name),
        })

    tags = []
    terms = Term.query.filter_by(site=site, type='tag').order_by('name').all()
    for term in terms:
        tags.append({
            'name': term.name,
            'desc': term.desc,
            'link': url_for('post_page.paginate_with_term_tag', term=term.name),
        })

    widgets = {
        'categories': categories,
        'tags': tags,
        'date_years': _widget_date_year(),
    }

    return widgets


def _widget_date_year():
    """"""
    date_years = {}

    for post in Post.query.filter_by(type='blog', published=True):
        year = post.published_time.year

        if year not in date_years:
            date_years[year] = {
                'display': str(year),
                'link': url_for('post_page.paginate_with_year', year=year),
                'count': 1,
            }

        date_years[year]['count'] += 1

    return date_years


def _post_info(post):
    """"""
    categorys = []
    tags = []
    for term in post.terms:
        if term.type == 'category':
            categorys.append(term.name)
        elif term.type == 'tag':
            tags.append(term.name)

    if post.type == 'page':
        link = url_for('post_page.one_with_name', post_name=post.name)
    else:
        link = url_for('post_page.one_with_id', post_id=post.id)

    return {
        'title': post.title,
        'uuid': post.id,
        'type': post.type,
        'author': post.author.name,
        'author_id': post.author.id,
        'published_time': post.published_time,
        'excerpt': post.content[:50],
        'content': post.content,
        'categorys': categorys,
        'tags': tags,
        'allow_comment': post.allow_comment,
        'link': link,
    }


def _post_term(term, paginate):
    """"""
    site = get_current_request_site()

    query = Post.query.filter_by(
        site=site, type=POST.TYPE.BLOG, published=True
    ).filter(Post.terms.any(name=term)).order_by(desc('published_time'))

    paginate['key'] = term
    paginate['title'] = term  # TODO!!!diaplay name?
    return _render_paginate_post_page(query, paginate)


def _render_paginate_post_page(query, paginate):
    """"""
    post_paginate = query.paginate(paginate['curr_num'], per_page=10)

    paginate['has_prev'] = post_paginate.has_prev
    paginate['has_next'] = post_paginate.has_next
    paginate['prev_num'] = post_paginate.prev_num
    paginate['next_num'] = post_paginate.next_num

    paginate_posts = []
    for post in post_paginate.items:
        paginate_posts.append(_post_info(post))
    paginate['posts'] = paginate_posts

    widgets = _sidebar()

    content = {
        'paginate': paginate,
        'widgets': widgets,
    }

    return render_template('post_paginate.html', content=content)


def _render_one_post(post):
    """render one post"""
    content = {
        'post': _post_info(post),
    }

    comment_list = []
    comments = Comment.query.filter_by(post=post).order_by(desc('created_time')).all()
    for comment in comments:
        comment_list.append({
            'commenter_name': comment.commenter_name,
            'created_time': comment.created_time,
            'content': comment.content,
        })
    content['comments'] = comment_list

    return render_template('post.html', content=content)


@post_page.route('/', methods=['GET'])
@post_page.route('/paginate/<int:page_num>', methods=['GET'])
def paginate_with_all(page_num=1):
    """"""
    site = get_current_request_site()

    query = Post.query.filter_by(site=site, type='blog', published=True).order_by(desc('published_time'))
    paginate = {
        'title': 'Home',  # TODO需要改为站点相关信息
        'curr_num': page_num,
        'view_name': 'post_page.paginate_with_all',
    }

    return _render_paginate_post_page(query, paginate)


@post_page.route('/date/<int:year>', methods=['GET'])
@post_page.route('/date/<int:year>/paginate/<int:page_num>', methods=['GET'])
def paginate_with_year(year, page_num=1):
    """"""
    site = get_current_request_site()

    query = Post.query.filter_by(
        site=site, type='blog', published=True
    ).filter(
        Post.published_time >= datetime(year, 1, 1), Post.published_time < datetime(year + 1, 1, 1)
    ).order_by(desc('published_time'))
    paginate = {
        'title': year,
        'key': year,
        'desc': 'Viewing the date archives',
        'curr_num': page_num,
        'view_name': 'post_page.paginate_with_year',
    }

    return _render_paginate_post_page(query, paginate)


@post_page.route('/category/<string:term>', methods=['GET'])
@post_page.route('/category/<string:term>/paginate/<int:page_num>', methods=['GET'])
def paginate_with_term_category(term, page_num=1):
    """"""
    paginate = {
        'desc': 'Viewing the category',
        'curr_num': page_num,
        'view_name': 'post_page.paginate_with_term_category',
    }

    return _post_term(term, paginate)


@post_page.route('/tag/<string:term>', methods=['GET'])
@post_page.route('/tag/<string:term>/paginate/<int:page_num>', methods=['GET'])
def paginate_with_term_tag(term, page_num=1):
    """"""
    paginate = {
        'desc': 'Viewing the tag',
        'curr_num': page_num,
        'view_name': 'post_page.paginate_with_term_tag',
    }

    return _post_term(term, paginate)


@post_page.route('/author/<string:author>', methods=['GET'])
@post_page.route('/author/<string:author>/paginate/<int:page_num>', methods=['GET'])
def paginate_with_author(author, page_num=1):
    """"""
    site = get_current_request_site()

    query = Post.query.filter_by(site=site, type='blog', published=True).filter(
        Post.author.has(User.name == author)).order_by(desc('published_time'))
    paginate = {
        'title': author,  # TODO!!!display name
        'curr_num': page_num,
        'view_name': 'post_page.paginate_with_author',
    }

    return _render_paginate_post_page(query, paginate)


@post_page.route("/search/")
@post_page.route("/search/paginate/<int:page_num>/")
def paginate_with_search(page_num=1):
    """"""
    site = get_current_request_site()
    keywords = request.args.get('keywords', '').strip(',')

    if not keywords:
        return redirect(url_for("post_page.index"))

    post_query = Post.query.search(site=site, keywords=keywords)  # TODO!!!!当前搜索多个关键字有bug

    if post_query.count() == 1:
        # only one result
        posts = post_query.all()
        post = posts[0]
        return redirect(url_for('post_page.one_with_id', post_id=post.id))

    paginate = {
        'title': keywords,
        'key': keywords,
        'desc': 'Search results for',
        'curr_num': page_num,
        'view_name': 'post_page.paginate_with_search',

        'keywords': keywords,
    }

    return _render_paginate_post_page(post_query, paginate)


@post_page.route('/post/<uuid:post_id>', methods=['GET', ])
def one_with_id(post_id):
    """"""
    site = get_current_request_site()

    post = Post.query.filter_by(site=site, id=post_id, published=True).first_or_404()
    return _render_one_post(post)


@post_page.route('/<string:post_name>', methods=['GET', ])
def one_with_name(post_name):
    """"""
    site = get_current_request_site()

    post = Post.query.filter_by(site=site, name=post_name, published=True, type='page').first_or_404()
    return _render_one_post(post)
