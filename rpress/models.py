#!/usr/bin/env python
#coding=utf-8


from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship  #, backref

from rpress.database import db
from rpress.helpers.uuid1plus import uuid1plus2datetime


########################################################################
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    password = Column(String(256))
    email = Column(String(120), unique=True)
    display = Column(String(50))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


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
    publish_ext = Column(String(8), default='unknow')  #publish 为 True 时才有意义。unknow, publish, draft/autosave/history/trash

    allow_comment = Column(Boolean, default=True)

    type = Column(String(4), default='blog')  #blog/page
    name = Column(String(50))
    terms = relationship("Term",
                        secondary=post_term_relations,
                        backref="posts")

    title = Column(String(50))
    content = Column(Text)

    #----------------------------------------------------------------------
    def __init__(self, uuid, creater_id, create_date=None, publish=True, publish_ext='publish', type='blog', name=None, title=None, content=None):
        """Constructor"""
        if create_date is None:
            create_date = uuid1plus2datetime(uuid)

        self.uuid = str(uuid)

        self.creater_id = creater_id
        self.create_date = create_date
        self.updater_id = creater_id
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
    def __init__(self, name, type='tag'):
        """Constructor"""
        self.name = name
        self.type = type

        self.display = name
        return

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<Term %r>' % (self.name)
