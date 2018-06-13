#!/usr/bin/env python
# coding=utf-8


import datetime
import codecs
import json

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
            'id': post.uuid,
            'type': post.type,

            'author': user_map_id_to_name[post.author_id],
            'reviser': None if post.updater_id is None else user_map_id_to_name[post.updater_id],

            'published': post.published,
            'publish_status': post.publish_state,

            'created_time': post.publish_date.isoformat(),
            'published_time': post.publish_date.isoformat(),
            'updated_time': None if post.update_date is None else post.update_date.isoformat(),

            'name': post.name,
            'title': post.title,
            'content': post.content,

            'allow_comment': post.allow_comment,

            'terms': {
                'category': [],
                'tag': [],
            },

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
