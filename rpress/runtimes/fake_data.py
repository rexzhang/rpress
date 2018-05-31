#!/usr/bin/env python
# coding=utf-8


from rpress import db
from rpress.constants import PUBLISH_FSM_DEFINE
from rpress.models import User, Site, SiteSetting, Post


def add_sample_user_and_site(user_name, user_password, site_domain_name):
    user = User.query.filter_by(name=user_name).first()
    if user is not None:
        print('duplicate user name!')
        return None

    user = User(name=user_name, password=user_password)
    db.session.add(user)
    
    site = Site(domain=site_domain_name)
    db.session.add(site)

    site_titel = SiteSetting(site=site, key='title', value='rPress Site')
    db.session.add(site_titel)
    site_desc = SiteSetting(site=site, key='desc', value='a new rPress site')
    db.session.add(site_desc)

    blog = Post(
        site=site, author=user_name,
        published=True, publish_state=PUBLISH_FSM_DEFINE.STATE.PUBLISHED, type='blog',
        title=u'this is first blog', content=u'i am blog content'
    )
    db.session.add(blog)
    page = Post(
        site=site, author=user_name,
        published=True, publish_state=PUBLISH_FSM_DEFINE.STATE.PUBLISHED, type='page',
        name='sample', title=u'this is first page', content=u'i am page'
    )
    db.session.add(page)

    db.session.commit()
    return 
