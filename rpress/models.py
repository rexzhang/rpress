#!/usr/bin/env python
#coding=utf-8


from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey

from rpress.database import db


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
class Post(db.Model):
    """"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    #site id

    creater = Column(Integer, ForeignKey('users.id'), default=1)  #暂时定义 user_id＝＝0 为异常归属
    updater = Column(Integer, ForeignKey('users.id'), default=1)

    publish = Column(Boolean, default=False)
    publish_ext = Column(String(8), default='unknow')  #unknow, publish, draft/autosave/history/trash

    allow_comment = Column(Boolean, default=True)

    type = Column(String(4), default='blog')  #blog/page
    name = Column(String(50), unique=True)

    title = Column(String(50))
    content = Column(Text)

    #----------------------------------------------------------------------
    def __init__(self, title=None, content=None):
        """Constructor"""
        self.title = title
        self.content = content
        return

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<Post %r>' % (self.title)




