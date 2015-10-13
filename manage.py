#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import


#from flask import Flask
#from flask import current_app
from flask.ext.script import Manager, prompt_bool, prompt

from rpress import create_app
from rpress import db
from rpress.helpers.uuid1plus import uuid1fromdatetime
from rpress.helpers.importer import convert_code_tag


manager = Manager(create_app())


#----------------------------------------------------------------------
@manager.command
def init_db(defaultdate=False):
    """不能正常工作，可能是当前缺少 model 关联操作"""
##    app.request_context()
##    with app.app_context():
    from rpress.models import User, Site, Post

    db.create_all()

    if defaultdate:
        user = User(name='rex', password='rexzhang')
        db.session.add(user)

        site = Site(name='rexzhangname', title='Rex.Zhang.name', desc='从记录到不仅仅是记录')
        db.session.add(site)

        post = Post(creater=user, publish=True, publish_ext='publish', title=u'这是第一篇博客', content=u'我是博客内容')
        db.session.add(post)
        db.session.commit()

    return


@manager.option('-c', '--disable_convert_code_tag', default=False)
#----------------------------------------------------------------------
def importer(disable_convert_code_tag):
    """"""
    import HTMLParser
    from datetime import datetime
    import feedparser

    from rpress.models import User, Post, Term, Comment

    def datetime_from_str(string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def convert_content(content):
        html_parser = HTMLParser.HTMLParser()
        content = html_parser.unescape(content)

        if not disable_convert_code_tag:
            content = convert_code_tag(content)
        return content

    def create_new_user(username):
        """create a user with cannot login"""
        prompt('user name:', default=username)

        user = User(name=username)
        db.session.add(user)
        return user

    #init data
    term_name_category_list = []
    categorys = Term.query.filter_by(type='category').all()
    for category in categorys:
        term_name_category_list.append(category.name)

    term_name_tag_list = []
    tags = Term.query.filter_by(type='tag').all()
    for tag in tags:
        term_name_tag_list.append(tag.name)

    import_wp_past_type_list = ['post', 'page']

    print('loading RSS file...')
    wordpress_data = feedparser.parse('rexzhangname.wordpress.2015-09-18.xml')

    print('parsering RSS file...')
    skip_author_set = set()
    for entry in wordpress_data.entries:
        #print(entry.wp_post_id, entry.wp_post_type, entry.wp_status, entry.author, entry.title, ' --- ', entry.wp_post_name)
        #某些条目内同时包含 post 和 comment 信息

        if entry.wp_post_type not in import_wp_past_type_list:
            #skip some post
            continue

        #create datetime
        post_create_date = datetime_from_str(entry.wp_post_date)

        #skip duplicate post: title + post_create_date
        exist_posts = Post.query.filter_by(title=entry.title, create_date=post_create_date).all()
        if len(exist_posts) >= 1:
            print('[wrong] skip duplicate post:%s' % entry.title)
            continue

        #check author
        is_skip_author = False
        if entry.author in skip_author_set:
            is_skip_author = True
        else:
            user = User.query.filter_by(name=entry.author).first()
            if user is None:
                if prompt_bool('Found new author:[%s], did you create user?' % entry.author, default=True):
                    user = create_new_user(entry.author)
                else:
                    skip_author_set.add(entry.author)
                    is_skip_author = True

        #skip author
        if is_skip_author:
            print('[wrong] miss user:[%s], skip post;%s' % (entry.author, entry.title))
            continue

        #publish status
        if entry.wp_status == 'publish':
            publish = True
            publish_ext = 'publish'
        elif entry.wp_status == 'draft':
            publish = False
            publish_ext = 'draft'
        else:
            continue

        #post type
        if entry.wp_post_type == 'post':
            type = 'blog'
        elif entry.wp_post_type == 'page':
            type = 'page'
        else:
            continue

        #post content
        if entry.content[0].type == 'text/html':
            content = convert_content(entry.content[0].value)

        print('+ %s %s' % (publish_ext, entry.title))
        post = Post(creater=user,
                    create_date=post_create_date,
                    publish=publish, publish_ext=publish_ext,
                    type=type,
                    name=entry.wp_post_name.lower(),
                    title=entry.title,
                    content=content)

        db.session.add(post)

        #terms
        #允许 category 与 tag 之间重名, rPress 不允许重名
        if not hasattr(entry, 'tags'):
            #can not found tags item
            continue

        for term in entry.tags:
            new_term = False
            term_name = term.term.lower()

            if term.scheme == 'category':
                term_type = 'category'

                if term_name not in term_name_category_list:
                    term_name_category_list.append(term_name)
                    new_term = True

            elif term.scheme == 'post_tag':
                term_type = 'tag'

                if term_name not in term_name_tag_list:
                    term_name_tag_list.append(term_name)
                    new_term = True

            else:
                #some error
                continue

            if new_term:
                term = Term(term_name, type=term_type, display=term.term)
                db.session.add(term)
            else:
                term = Term.query.filter_by(name=term_name).first()

            post.terms.append(term)

    #comment
    for entry in wordpress_data.entries:
        if not hasattr(entry, 'wp_comment_date'):
            #skip, if it is't comment
            continue

        #comment create date
        comment_create_date=datetime_from_str(entry.wp_comment_date)

        #skip duplicate comment: author + comment_create_date
        exist_commnets = Comment.query.filter_by(author_name=entry.wp_comment_author, create_date=comment_create_date).all()
        if len(exist_commnets) >= 1:
            print('[wrong] skip duplicate comment:[%s] %s' % (entry.wp_comment_author, entry.wp_comment_date))
            continue

        post_create_date = datetime_from_str(entry.wp_post_date)
        post = Post.query.filter_by(title=entry.title, create_date=post_create_date).first()
        if post is None:
            print('[wrong] miss post, comment:[%s] %s' % (entry.wp_comment_author, entry.wp_comment_date))
            continue

        print('+ comment %s %s' % (entry.wp_comment_date, entry.wp_comment_author))
        comment = Comment(post=post,
                author_name=entry.wp_comment_author,
                create_date=comment_create_date,
                content=convert_content(entry.wp_comment_content),
                author_email=entry.wp_comment_author_email,
                author_ip=entry.wp_comment_author_ip,
                author_url=entry.wp_comment_author_url)

        db.session.add(comment)

    #commit
    db.session.commit()
    return


#----------------------------------------------------------------------
def main():
    """"""
    manager.run()

    return


if __name__ == "__main__":
    main()
