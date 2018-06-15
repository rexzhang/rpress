#!/usr/bin/env python
# coding=utf-8


from datetime import datetime

from rpress.constants import POST, TERM, PUBLISH_FSM_DEFINE
from rpress.models import User, Site, SiteSetting, Post, Term, Comment
from rpress.database import db
from rpress.runtimes.password import generate_password_hash


def add_sample_user_and_site(user_name, user_password, site_domain_name):
    session = db.session()

    user = User.query.filter_by(name=user_name).first()
    if user is not None:
        print('duplicate user name!')
        return None

    user = User(name=user_name, password=generate_password_hash(user_password))
    session.add(user)

    site = Site(domain=site_domain_name)
    session.add(site)

    session.flush()

    site_title = SiteSetting(site_id=site.id, key='title', value='rPress Site')
    site_desc = SiteSetting(site_id=site.id, key='desc', value='a new rPress site')
    session.add(site_title)
    session.add(site_desc)

    session.flush()

    blog = Post(
        site_id=site.id, author_id=user.id, type=POST.TYPE.BLOG,
        published=True, publish_status=PUBLISH_FSM_DEFINE.STATE.PUBLISHED, published_time=datetime.now(),
        title='this is first blog', content='i am blog content'
    )
    session.add(blog)
    page = Post(
        site_id=site.id, author_id=user.id, type=POST.TYPE.PAGE,
        published=True, publish_status=PUBLISH_FSM_DEFINE.STATE.PUBLISHED, published_time=datetime.now(),
        name='sample', title='this is first page', content='i am page'
    )
    session.add(page)

    session.flush()

    comment = Comment(post_id=blog.id, author_name='a man', content='this is comment')
    session.add(comment)

    term_category = Term(site_id=site.id, name=TERM.TYPE.CATEGORY, type=TERM.TYPE.CATEGORY)
    term_tag = Term(site_id=site.id, name=TERM.TYPE.TAG, type=TERM.TYPE.TAG)
    session.add(term_category)
    session.add(term_tag)

    return
