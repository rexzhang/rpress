#!/usr/bin/env python
# coding=utf-8


from rpress.constants import PUBLISH_FSM_DEFINE
from rpress.models import User, Site, SiteSetting, Post
from rpress.database import db


def add_sample_user_and_site(user_name, user_password, site_domain_name):
    session = db.session()
    
    user = User.query.filter_by(name=user_name).first()
    if user is not None:
        print('duplicate user name!')
        return None

    user = User(name=user_name, password=user_password)
    session.add(user)
    
    site = Site(domain=site_domain_name)
    session.add(site)

    site_title = SiteSetting(site=site, key='title', value='rPress Site')
    session.add(site_title)
    site_desc = SiteSetting(site=site, key='desc', value='a new rPress site')
    session.add(site_desc)

    blog = Post(
        site=site, author=user, type='blog', published=True, publish_state=PUBLISH_FSM_DEFINE.STATE.PUBLISHED,
        title='this is first blog', content='i am blog content'
    )
    session.add(blog)
    page = Post(
        site=site, author=user, type='page', published=True, publish_state=PUBLISH_FSM_DEFINE.STATE.PUBLISHED,
        name='sample', title='this is first page', content='i am page'
    )
    session.add(page)
    return
