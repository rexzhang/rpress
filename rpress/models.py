#!/usr/bin/env python
#coding=utf-8


from sqlalchemy import Column, Integer, String, Text

from rpress.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


########################################################################
class Blog(db.Model):
    """"""
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True)

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
        return '<Blog %r>' % (self.title)




