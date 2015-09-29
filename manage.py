#!/usr/bin/env python
#coding=utf-8


import hashlib

from flask import Flask
from flask import current_app
from flask.ext.script import Manager

from rpress import create_app
from rpress import db


manager = Manager(create_app())


#----------------------------------------------------------------------
@manager.command
def init_db():
    """不能正常工作，可能是当前缺少 model 关联操作"""
##    app.request_context()
##    with app.app_context():
    from rpress.models import User, Post
    db.create_all()

    u = User(name='admin', password=hashlib.sha256('admin').hexdigest())
    db.session.add(u)
    db.session.commit()

    p = Post(title=u'这是第一篇博客', content=u'我是博客内容')
    db.session.add(p)
    db.session.commit()

    return


#----------------------------------------------------------------------
def main():
    """"""
    manager.run()

    return


if __name__ == "__main__":
    main()