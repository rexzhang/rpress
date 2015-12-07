#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import re
import HTMLParser
from datetime import datetime

import feedparser

from rpress.models import User, Site, SiteSetting, Post, Term, Comment
from rpress.helpers.fsm import PublishFSM


#----------------------------------------------------------------------
def add_site_sample_data(db_session, site_domain, admin_user):
    """add site's sample data into db"""
    site = Site(domain=site_domain)
    db_session.add(site)

    site_titel = SiteSetting(site=site, key='title', value='rPress Site')
    db_session.add(site_titel)
    site_desc = SiteSetting(site=site, key='desc', value='a new rPress site')
    db_session.add(site_desc)

    blog = Post(author=admin_user, site=site, published=True, publish_state=PublishFSM.STATE_PUBLISHED, type='blog', title=u'this is first blog', content=u'i am blog content')
    db_session.add(blog)
    page = Post(author=admin_user, site=site, published=True, publish_state=PublishFSM.STATE_PUBLISHED, type='page', name='sample', title=u'this is first page', content=u'i am page')
    db_session.add(page)
    return


#----------------------------------------------------------------------
def convert_code_tag(string):
    """
    convert code tag:
    [language_name]xxx[/language_name] to:
    [code:language_name]xxx[/code]
    """
    code_name_list = list(set(re.findall('\[/([a-z]+?)\]', string)))
    #print('found code name:%r' % code_name_list)

    for code_name in code_name_list:
        string = re.sub('\[%s\]\n' % code_name, '[code:%s]\n' % code_name, string)
        string = re.sub('\n\[/%s\]' % code_name, '\n[/code]', string)

    return string


#----------------------------------------------------------------------
def import_site_from_wordpress(db_session, site, disable_convert_code_tag, filename):
    """"""
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
        user_name = prompt('user name:', default=username)

        user = User(name=user_name)
        db_session.add(user)
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
    wordpress_data = feedparser.parse(filename)

    print('parsering RSS file...')
    skip_author_set = set()
    for entry in wordpress_data.entries:
        #print(entry.wp_post_id, entry.wp_post_type, entry.wp_status, entry.author, entry.title, ' --- ', entry.wp_post_name)
        #某些条目内同时包含 post 和 comment 信息

        if entry.wp_post_type not in import_wp_past_type_list:
            #skip some post
            continue

        #create datetime
        post_publish_date = datetime_from_str(entry.wp_post_date)

        #skip duplicate post: title + post_publish_date
        exist_posts = Post.query.filter_by(title=entry.title, publish_date=post_publish_date).all()
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
            published = True
            publish_state = PublishFSM.STATE_PUBLISHED
        elif entry.wp_status == 'draft':
            published = False
            publish_state = PublishFSM.STATE_DRAFT
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

        print('+ %s %s' % (publish_state, entry.title))
        post = Post(author=user, site=site,
                    published=published, publish_state=publish_state, publish_date=post_publish_date,
                    type=type,
                    name=entry.wp_post_name.lower(),
                    title=entry.title,
                    content=content)

        db_session.add(post)

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
                term = Term(site, term_name, type=term_type)
                db_session.add(term)
            else:
                term = Term.query.filter_by(name=term_name).first()

            post.terms.append(term)

    #comment
    for entry in wordpress_data.entries:
        if not hasattr(entry, 'wp_comment_date'):
            #skip, if it is't comment
            continue

        #comment create date
        comment_publish_date=datetime_from_str(entry.wp_comment_date)

        #skip duplicate comment: author + comment_publish_date
        exist_commnets = Comment.query.filter_by(author_name=entry.wp_comment_author, publish_date=comment_publish_date).all()
        if len(exist_commnets) >= 1:
            print('[wrong] skip duplicate comment:[%s] %s' % (entry.wp_comment_author, entry.wp_comment_date))
            continue

        post_publish_date = datetime_from_str(entry.wp_post_date)
        post = Post.query.filter_by(title=entry.title, publish_date=post_publish_date).first()
        if post is None:
            print('[wrong] miss post, comment:[%s] %s' % (entry.wp_comment_author, entry.wp_comment_date))
            continue

        print('+ comment %s %s' % (entry.wp_comment_date, entry.wp_comment_author))
        comment = Comment(post=post,
                author_name=entry.wp_comment_author,
                publish_date=comment_publish_date,
                content=convert_content(entry.wp_comment_content),
                author_email=entry.wp_comment_author_email,
                author_ip=entry.wp_comment_author_ip,
                author_url=entry.wp_comment_author_url)

        db_session.add(comment)
    return
