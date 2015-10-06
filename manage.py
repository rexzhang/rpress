#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import hashlib

#from flask import Flask
#from flask import current_app
from flask.ext.script import Manager

from rpress import create_app
from rpress import db
from rpress.helpers.uuid1plus import uuid1plus


manager = Manager(create_app())


#----------------------------------------------------------------------
@manager.command
def init_db():
    """不能正常工作，可能是当前缺少 model 关联操作"""
    from datetime import datetime
##    app.request_context()
##    with app.app_context():
    from rpress.models import User, Post

    db.create_all()

    user = User(name='rex', password=hashlib.sha256('rexzhang').hexdigest())
    db.session.add(user)
    db.session.commit()

    post = Post(uuid=uuid1plus(datetime.now()), creater_id=user.id, title=u'这是第一篇博客', content=u'我是博客内容')
    db.session.add(post)
    db.session.commit()

    return


#----------------------------------------------------------------------
@manager.command
def import_wordpress():
    """"""
    import HTMLParser
    from datetime import datetime
    import feedparser

    from rpress.models import User, Post, Term  #, TermRelation

    html_parser = HTMLParser.HTMLParser()
    term_name_category_list = []
    term_name_tag_list = []

    import_wp_past_type_list = ['post', 'page']

    print('loading RSS file...')
    wordpress_data = feedparser.parse('rexzhangname.wordpress.2015-09-18.xml')

    print('parsering RSS file...')
    for entry in wordpress_data.entries:
        #print(entry.wp_post_id, entry.wp_post_type, entry.wp_status, entry.author, entry.title, ' --- ', entry.wp_post_name)
        ##!!!还有一个多次导入排除重复的问题，使用创建时间＋文章标题？

        if entry.wp_post_type not in import_wp_past_type_list:
            #skip some post
            continue

        #uuid
        uuid = uuid1plus(datetime.strptime(entry.wp_post_date, "%Y-%m-%d %H:%M:%S"))

        #author
        user = User.query.filter_by(name=entry.author).first()
        if user is None:
            print('!!!ERROR!!miss user:%s, skip one post;%s' % (entry.author, entry.title))
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
            content = html_parser.unescape(entry.content[0].value)

        print('+ %s %s' % (publish_ext, entry.title))
        post = Post(uuid=uuid,
                    creater_id=user.id,
                    publish=publish, publish_ext=publish_ext,
                    type=type,
                    name=entry.wp_post_name,
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
            term_name = term.term

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
                term = Term(term_name, type=term_type)
                db.session.add(term)
            else:
                term = Term.query.filter_by(name=term_name).first()

            post.terms.append(term)

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
