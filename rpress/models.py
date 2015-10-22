#!/usr/bin/env python
#coding=utf-8


import hashlib

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship  #, backref
from flask.ext.sqlalchemy import BaseQuery

from rpress.database import db
from rpress.helpers.uuid1plus import uuid1, uuid1fromdatetime
from rpress.helpers.fsm import PublishFSM


########################################################################
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    _password = Column('password', String(256))
    email = Column(String(32), unique=True)
    display = Column(String(50))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)

    #----------------------------------------------------------------------
    def _password_get(self):
        """"""
        return self._password

    #----------------------------------------------------------------------
    def _password_set(self, password):
        """"""
        if password is None:
            self._password = ''
        else:
            self._password = hashlib.sha256(password).hexdigest()
        return

    #----------------------------------------------------------------------
    def password_validate(self, password=None):
        """check user's password"""
        if password is not None and hashlib.sha256(password).hexdigest() == self._password:
            return True

        return False

    password = db.synonym("_password", descriptor=property(fget=_password_get, fset=_password_set))


########################################################################
post_term_relations = db.Table('post_term_relations',
    db.Column('term_id', db.Integer, db.ForeignKey('terms.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)


########################################################################
class PostQuery(BaseQuery):
    """"""
    #----------------------------------------------------------------------
    def search(self, keywords):
        """"""
        criteria = []

        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(Post.title.ilike(keyword),
                                   Post.name.ilike(keyword),
                                   Post.content.ilike(keyword),
                                   #Post.terms.ilike(keyword)
                                   ))

        query = reduce(db.and_, criteria)
        return self.filter(query)


########################################################################
class Post(db.Model):
    """"""
    query_class = PostQuery

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True)
    #site id

    author_id = Column(Integer, ForeignKey('users.id'), default=0)  #暂时定义 user_id＝＝0 为异常归属
    author = relationship('User', foreign_keys=[author_id])

    published = Column(Boolean, default=False)
    publish_state = Column(String(20), default=PublishFSM.STATE_DEFAULT)  #published 为 True 时才有意义 #修改过程版本存放在另外一个表中
    publish_date = Column(DateTime)

    updater_id = Column(Integer, ForeignKey('users.id'))
    updater = relationship('User', foreign_keys=[updater_id])
    update_date = Column(DateTime)

    allow_comment = Column(Boolean, default=True)

    type = Column(String(4), default='blog')  #blog/page
    name = Column(String(128))
    terms = relationship("Term",
                        secondary=post_term_relations,
                        backref="posts")

    title = Column(String(128))
    content = Column(Text)

    #----------------------------------------------------------------------
    def __init__(self, author, uuid=None, publish_date=None, published=False, publish_state=PublishFSM.STATE_DRAFT, type='blog', name=None, title=None, content=None):
        """Constructor"""
        if uuid is None and publish_date is None:
            uuid = uuid1()
            publish_date = uuid.datetime

        elif uuid is not None and publish_date is None:
            publish_date = uuid.datetime

        elif uuid is None and publish_date is not None:
            uuid = uuid1fromdatetime(publish_date)

        self.uuid = str(uuid)

        self.author = author

        self.published = published
        self.publish_state = publish_state
        self.publish_date = publish_date

        self.updater = author
        self.update_date = publish_date

        self.type = type
        self.name = name  #!!!convert title to %xx if name==None

        self.title = title
        self.content = content
        return

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<Post %r>' % (self.title)  #!!!


########################################################################
class Term(db.Model):
    """"""
    __tablename__ = 'terms'

    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True)
    type = Column(String(50))  #tag/category
    desc = Column(Text)

    #----------------------------------------------------------------------
    def __init__(self, name, type='tag', desc=None):
        """Constructor"""
        self.name = name
        self.type = type
        self.desc = desc
        return

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<Term %r>' % (self.name)


########################################################################
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

    #----------------------------------------------------------------------
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

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<Comment %r>' % (self.author_name)  #!!!


########################################################################
class Site(db.Model):
    """"""
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    title = Column(String(50))
    desc = Column(String(128))

    #----------------------------------------------------------------------
    def __init__(self, name, title, desc=None):
        """Constructor"""
        self.name = name

        self.title = title
        self.desc = desc
        return

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<Site %r>' % (self.title)
