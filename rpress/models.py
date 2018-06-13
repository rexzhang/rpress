#!/usr/bin/env python
# coding=utf-8


import hashlib

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import BaseQuery

from rpress.constants import PUBLISH_FSM_DEFINE
from rpress.database import db
from rpress.helpers.uuid1plus import uuid1, uuid1_from_datetime


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    _password = Column('password', String(256))
    email = Column(String(32), unique=True)
    display = Column(String(50), unique=True)

    def __repr__(self):
        return '<User:{}|{}>'.format(self.id, self.name)

    def _password_get(self):
        return self._password

    def _password_set(self, password):
        if password is None:
            self._password = ''
        else:
            self._password = hashlib.sha256(bytes(password, 'utf8')).hexdigest()
        return

    def password_validate(self, password=None):
        """check user's password"""
        if password is not None and hashlib.sha256(str(password, 'utf8')).hexdigest() == self._password:
            return True

        return False

    password = db.synonym("_password", descriptor=property(fget=_password_get, fset=_password_set))


post_term_relations = db.Table('post_term_relations',
                               db.Column('term_id', db.Integer, db.ForeignKey('terms.id')),
                               db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                               )


class PostQuery(BaseQuery):
    """"""

    def search(self, site, keywords):
        """"""
        criteria = []

        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(Post.title.ilike(keyword),
                                   Post.name.ilike(keyword),
                                   Post.content.ilike(keyword),
                                   # Post.terms.ilike(keyword)
                                   ))

        query = reduce(db.and_, criteria)
        return self.filter_by(site=site).filter(query)


class Post(db.Model):
    """"""
    query_class = PostQuery

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True)

    site_id = Column(Integer, ForeignKey('sites.id'), default=0)  # 暂时定义 site_id 为异常归属
    site = relationship('Site', foreign_keys=[site_id])

    author_id = Column(Integer, ForeignKey('users.id'), default=0)  # 暂时定义 user_id＝＝0 为异常归属
    author = relationship('User', foreign_keys=[author_id])

    published = Column(Boolean, default=False)
    publish_state = Column(String(20),
                           default=PUBLISH_FSM_DEFINE.DEFAULT_STATE)  # published 为 True 时才有意义 #修改过程版本存放在另外一个表中
    publish_date = Column(DateTime)

    updater_id = Column(Integer, ForeignKey('users.id'))
    updater = relationship('User', foreign_keys=[updater_id])
    update_date = Column(DateTime)

    allow_comment = Column(Boolean, default=True)

    type = Column(String(4), default='blog')  # blog/page
    name = Column(String(128))
    terms = relationship(
        "Term",
        secondary=post_term_relations,
        backref="posts"
    )

    title = Column(String(128))
    content = Column(Text)

    def __init__(self, **kwargs):
        if 'publish_state' not in kwargs:
            kwargs['publish_state'] = PUBLISH_FSM_DEFINE.DEFAULT_STATE

        if 'type' not in kwargs:
            kwargs['type'] = 'blog'

        if 'uuid' not in kwargs and 'publish_date' not in kwargs:
            kwargs['uuid'] = uuid1()
            kwargs['publish_date'] = kwargs['uuid'].datetime
        elif 'uuid' in kwargs and 'publish_date' not in kwargs:
            kwargs['publish_date'] = kwargs['uuid'].datetime
        elif 'uuid' not in kwargs and 'publish_date' in kwargs:
            kwargs['uuid'] = uuid1_from_datetime(kwargs['publish_date'])
        kwargs['uuid'] = str(kwargs['uuid'])

        # TODO: !!!convert title to %xx if name==None
        super().__init__(**kwargs)
        return

    def __repr__(self):
        """"""
        return '<Post:{}|{}>'.format(self.id, self.title)


class Term(db.Model):
    """"""
    __tablename__ = 'terms'

    id = Column(Integer, primary_key=True)

    site_id = Column(Integer, ForeignKey('sites.id'), default=0)  # 暂时定义 site_id 为异常归属
    site = relationship('Site', foreign_keys=[site_id])

    name = Column(String(50))
    type = Column(String(50))  # tag/category
    desc = Column(Text)

    def __init__(self, site, name, type='tag', desc=None):
        """Constructor"""
        self.site = site

        self.name = name
        self.type = type
        self.desc = desc
        return

    def __repr__(self):
        """"""
        return '<Term:{}|{}>'.format(self.id, self.name)


class Comment(db.Model):
    """"""
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', foreign_keys=[post_id])

    author_name = Column(String(50))
    author_email = Column(String(32))
    author_ip = Column(String(19))
    author_url = Column(Text)

    publish_date = Column(DateTime)
    content = Column(Text)

    def __init__(self, post, author_name, publish_date, content, author_email=None, author_ip=None, author_url=None):
        """Constructor"""
        self.post = post

        self.author_name = author_name
        self.author_email = author_email
        self.author_ip = author_ip
        self.author_url = author_url

        self.publish_date = publish_date
        self.content = content
        return

    def __repr__(self):
        """"""
        return '<Comment:{}|{}>'.format(self.id, self.author_name)


class Site(db.Model):
    """"""
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True)

    domain = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        """"""
        return '<Site:{}|{}>'.format(self.id, self.domain)


class SiteSetting(db.Model):
    """"""
    __tablename__ = 'site_settings'

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id'), default=0)  # 暂时定义 user_id＝＝0 为异常归属
    site = relationship('Site', foreign_keys=[site_id])

    key = Column(String(128))
    value = Column(Text())

    def __init__(self, site, key, value):
        """Constructor"""
        self.site = site

        self.key = key
        self.value = value
        return

    def __repr__(self):
        """"""
        return '<SiteSetting:{}|{}>'.format(self.id, self.key)
