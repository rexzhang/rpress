#!/usr/bin/env python
# coding=utf-8


import datetime
import codecs
import json

from rpress.database import db
from rpress.models import User, Site, SiteSetting, Post, Term, Comment
from rpress.runtimes.password import generate_password_hash

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


def export_site_data_to_json(site_id):
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
            'id': post.id,
            'type': post.type,

            'author': user_map_id_to_name[post.author_id],
            'reviser': None if post.reviser_id is None else user_map_id_to_name[post.reviser_id],

            'created_time': post.created_time.isoformat(),
            'updated_time': None if post.update_date is None else post.update_date.isoformat(),

            'published': post.published,
            'publish_status': post.publish_status,
            'published_time': post.published_time.isoformat(),

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
                    'name': comment.author_name,
                    'email': comment.author_email,
                    'ip': comment.author_ip,
                    'url': comment.author_url,
                },

                'time': comment.publish_date.isoformat(),
                'content': comment.content,
            }
            post_data['comments'].append(comment_data)

        data['posts'].append(post_data)

    filename = '{}.{}.rpress.json'.format(site.domain, datetime.datetime.now().isoformat())
    with codecs.open(filename, 'w+', encoding='utf-8') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)

    return


def import_site_data_from_json(filename):
    session = db.session()

    # User
    user_map_name_to_id = {}
    for user in User.query:
        user_map_name_to_id[user.name] = user.id

    def get_user_id(user_name):
        if user_map_name_to_id.get(user_name) is None:
            new_user = User(
                name=user_name,
                password=generate_password_hash('password'),
            )
            session.add(new_user)

            session.flush()
            user_map_name_to_id[user_name] = new_user.id

        return user_map_name_to_id[user_name]

    with codecs.open(filename, encoding='utf-8') as fp:
        data = json.load(fp)

    # Site
    site = Site(domain=data['site']['domain'])
    session.add(site)
    session.flush()

    for key in data['site']['settings']:
        site_setting = SiteSetting(
            site_id=site.id,

            key=key,
            value=data['site']['settings'][key],
        )
        session.add(site_setting)

    # Term
    term_map_name_to_id = {
        'category': {},
        'tag': {},
    }
    for term in Term.query.filter_by(site_id=str(site.id), type='category'):
        term_map_name_to_id['category'][term.name] = term.id
    for term in Term.query.filter_by(site_id=str(site.id), type='tag'):
        term_map_name_to_id['tag'][term.name] = term.id

    new_term_type = ''
    new_term_name = None

    def get_term_id():
        if term_map_name_to_id[new_term_type].get(new_term_name) is None:
            new_term = Term(
                site_id=site.id,

                type=new_term_type,
                name=new_term_name,
            )
            session.add(new_term)

            session.flush()
            term_map_name_to_id[new_term_type][new_term_name] = new_term.id

        return term_map_name_to_id[new_term_type][new_term_name]

    # Comment
    new_comment_data = None

    def get_comment_id(post_id):
        comment = Comment.query.filter_by(
            post_id=post_id,
            created_time=new_comment_data['time'],

            commenter_name=new_comment_data['commenter']['name'],

            content=new_comment_data['content'],
        ).first()
        if comment is None:
            comment = Comment(
                post_id=post_id,
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
        post = Post(
            site_id=site.id,

            id=post_data['id'],
            type=post_data['type'],

            author_id=get_user_id(post_data['author']),
            reviser_id=None if post_data['reviser'] is None else get_user_id(post_data['reviser']),

            created_time=post_data['created_time'],
            updated_time=post_data['updated_time'],

            published=post_data['published'],
            publish_status=post_data['publish_status'],
            published_time=post_data['published_time'],

            name=post_data['name'],
            title=post_data['title'],
            content=post_data['content'],

            allow_comment=post_data['allow_comment'],
        )
        session.add(post)

        for new_term_type in ['category', 'tag']:
            for new_term_name in post_data['terms'][new_term_type]:
                get_term_id()

        for new_comment_data in post_data['comments']:
            get_comment_id(post_id=post.id)

    session.commit()
    return
