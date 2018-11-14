#!/usr/bin/env python
# coding=utf-8


import datetime
import json
from uuid import uuid4

from rpress.database import db
from rpress.models import User, Site, SiteSetting, Post, Term, Comment

"""
data_format = {
    'version': 1,

    'site': {
        'domain': 'rex.zhang.name',
        'settings': {
            'key': 'value'
        },
    }

    'posts': [
        'id': 'uuid-str',
        'type': 'blog/page',

        'author': 'rex',
        'reviser': 'rex',  # last reviser

        'published': True/False,
        'publish_status': 'PUBLISH_STATUS',

        'created_time': 'YYYY-MM-DD HH:MM:SS',
        'published_time: 'YYYY-MM-DD HH:MM:SS',  # first publish time
        'updated_time': 'YYYY-MM-DD HH:MM:SS',  # last update time

        'name': 'xxx',
        'title': 'yyy',
        'content': 'zzz',

        'allow_comment': True/False,

        'terms': {
            'category': ['category1', 'category2],
            'tag': ['tag1', 'tag2],
        },

        'comments': [
            {
                'commenter': {
                    'name': 'xxx',
                    'email': 'rex.zhang@gmail.com',
                    'ip': '1.1.1.1',
                    'url': 'https://some.blog.site.com',
                },

                'time': 'YYYY-MM-DD HH:MM:SS',
                'content': 'zzz'
            },
            ...
            ...
            ...
        ],
        ...
        ...
        ...
    ]
}

"""


def export_site_data_to_json_str(site_id):
    site = Site.query.filter_by(id=site_id).first()
    if site is None:
        return

    data = {
        'version': 1,

        'site': {
            'domain': site.domain,
            'settings': {},
        },

        'posts': [],
    }

    user_map_id_to_name = {}
    for user in User.query:
        user_map_id_to_name[user.id] = user.name

    category_map_id_to_name = {}
    for term in Term.query.filter_by(type='category'):
        category_map_id_to_name[term.id] = term.name
    tag_map_id_to_name = {}
    for term in Term.query.filter_by(type='tag'):
        tag_map_id_to_name[term.id] = term.name

    for setting in SiteSetting.query.filter_by(site=site):
        data['site']['settings'][setting.key] = setting.value

    for post in Post.query.filter_by(site=site):
        post_data = {
            'id': str(post.id),
            'type': post.type,

            'author': user_map_id_to_name[post.author_id],
            'reviser': None if post.reviser_id is None else user_map_id_to_name[post.reviser_id],

            'created_time': post.created_time.isoformat(),
            'updated_time': None if post.updated_time is None else post.updated_time.isoformat(),

            'published': post.published,
            'publish_status': post.publish_status,
            'published_time': None if post.published_time is None else post.published_time.isoformat(),

            'name': post.name,
            'title': post.title,
            'content': post.content,

            'terms': {
                'category': [],
                'tag': [],
            },

            'allow_comment': post.allow_comment,
            'comments': [],
        }

        for term in post.terms:
            if term.type == 'category':
                post_data['terms']['category'].append(term.name)
            elif term.type == 'tag':
                post_data['terms']['tag'].append(term.name)

        for comment in Comment.query.filter_by(post=post):
            comment_data = {
                'commenter': {
                    'name': comment.commenter_name,
                    'email': comment.commenter_email,
                    'ip': comment.commenter_ip,
                    'url': comment.commenter_url,
                },

                'time': comment.created_time.isoformat(),
                'content': comment.content,
            }
            post_data['comments'].append(comment_data)

        data['posts'].append(post_data)

    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    filename = '{}.{}.rpress.json'.format(site.domain, datetime.datetime.now().strftime('%Y-%m-%d.%H-%M-%S.%f'))

    return json_str, filename


def import_site_data_from_json_fp(fp):
    session = db.session()
    post = None
    messages = []

    # parser json file
    data = json.load(fp)

    # User
    already_exists_users = {}
    for user in User.query:
        already_exists_users[user.name] = user

    def get_user_obj(user_name):
        if user_name not in already_exists_users:
            password = uuid4().hex
            messages.append('new user:{} password:{}'.format(user_name, password))

            new_user = User(
                name=user_name,
                password=password,
            )
            session.add(new_user)

            session.flush()
            already_exists_users[user_name] = new_user

        return already_exists_users[user_name]

    # Site
    if data.get('site') is None or data['site'].get('domain') is None:
        return

    domian = data['site']['domain']
    site = Site.query.filter_by(domain=domian).first()
    if site is None:
        site = Site(domain=domian)
        session.add(site)
        session.flush()

    # Site Settings
    for key in data['site']['settings']:
        site_setting = SiteSetting(
            site=site,

            key=key,
            value=data['site']['settings'][key],
        )
        session.add(site_setting)

    # Term
    already_exists_terms = {
        'category': {
            # key:name, value:obj
        },
        'tag': {
            # key:name, value:obj
        },
    }
    for term in Term.query.filter_by(site=site, type='category'):
        already_exists_terms['category'][term.name] = term
    for term in Term.query.filter_by(site=site, type='tag'):
        already_exists_terms['tag'][term.name] = term

    new_term_type = ''
    new_term_name = None

    def add_term_relationship():
        if new_term_name not in already_exists_terms[new_term_type]:
            new_term = Term(
                site=site,

                type=new_term_type,
                name=new_term_name,
            )
            session.add(new_term)

            session.flush()
            already_exists_terms[new_term_type][new_term_name] = new_term

        post.terms.append(already_exists_terms[new_term_type][new_term_name])
        return

    # Comment
    new_comment_data = None

    def add_comment():
        comment = Comment.query.filter_by(
            post=post,
            created_time=new_comment_data['time'],

            commenter_name=new_comment_data['commenter']['name'],

            content=new_comment_data['content'],
        ).first()
        if comment is None:
            comment = Comment(
                post=post,
                created_time=new_comment_data['time'],

                commenter_name=new_comment_data['commenter']['name'],
                commenter_email=new_comment_data['commenter']['email'],
                commenter_ip=new_comment_data['commenter']['ip'],
                commenter_url=new_comment_data['commenter']['url'],

                content=new_comment_data['content'],
            )
            session.add(comment)

        return comment.id

    for post_data in data['posts']:
        post = Post.query.filter_by(id=post_data['id']).first()
        if post is None:
            post = Post(site=site)

        post.id = post_data['id']
        post.type = post_data['type']

        post.author = get_user_obj(post_data['author'])
        post.reviser = None if post_data['reviser'] is None else get_user_obj(post_data['reviser'])

        post.created_time = post_data['created_time']
        post.updated_time = post_data['updated_time']

        post.published = post_data['published']
        post.publish_status = post_data['publish_status']
        post.published_time = post_data['published_time']

        post.name = post_data['name']
        post.title = post_data['title']
        post.content = post_data['content']

        post.allow_comment = post_data['allow_comment']

        session.add(post)

        for new_term_type in ['category', 'tag']:
            for new_term_name in post_data['terms'][new_term_type]:
                add_term_relationship()

        for new_comment_data in post_data['comments']:
            add_comment()

    session.commit()
    return messages
