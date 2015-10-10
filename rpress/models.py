#!/usr/bin/env python
#coding=utf-8


import hashlib

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship  #, backref

from rpress.database import db
from rpress.helpers.uuid1plus import uuid1, uuid1fromdatetime


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
class Post(db.Model):
    """"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True)
    #site id

    creater_id = Column(Integer, ForeignKey('users.id'), default=0)  #暂时定义 user_id＝＝0 为异常归属
    updater_id = Column(Integer, ForeignKey('users.id'))
    creater = relationship('User', foreign_keys=[creater_id])
    updater = relationship('User', foreign_keys=[updater_id])
    create_date = Column(DateTime)
    update_date = Column(DateTime)

    publish = Column(Boolean, default=False)
    publish_ext = Column(String(8), default='unknow')  #publish 为 True 时才有意义。unknow, publish, draft/autosave/history/trash #修改过程版本存放在另外一个表中

    allow_comment = Column(Boolean, default=True)

    type = Column(String(4), default='blog')  #blog/page
    name = Column(String(128))
    terms = relationship("Term",
                        secondary=post_term_relations,
                        backref="posts")

    title = Column(String(128))
    content = Column(Text)

    #----------------------------------------------------------------------
    def __init__(self, creater, uuid=None, create_date=None, publish=False, publish_ext='draft', type='blog', name=None, title=None, content=None):
        """Constructor"""
        if uuid is None and create_date is None:
            uuid = uuid1()
            create_date = uuid.datetime

        elif uuid is not None and create_date is None:
            create_date = uuid.datetime

        elif uuid is None and create_date is not None:
            uuid = uuid1fromdatetime(create_date)

        self.uuid = str(uuid)

        self.creater = creater
        self.updater = creater

        self.create_date = create_date
        self.update_date = create_date

        self.publish = publish
        self.publish_ext = publish_ext

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
    display = Column(String(50))

    #----------------------------------------------------------------------
    def __init__(self, name, type='tag', display=None):
        """Constructor"""
        self.name = name
        self.type = type

        if display is None:
            self.display = name
        else:
            self.display = display

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

    create_date = Column(DateTime)
    content = Column(Text)

    #----------------------------------------------------------------------
    def __init__(self, post, author_name, create_date, content, author_email=None, author_ip=None, author_url=None):
        """Constructor"""
        self.post = post

        self.author_name = author_name
        self.author_email = author_email
        self.author_ip = author_ip
        self.author_url = author_url

        self.create_date = create_date
        self.content = content
        return

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<Comment %r>' % (self.author_name)  #!!!


