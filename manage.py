#!/usr/bin/env python
#coding=utf-8


from flask import Flask
from flask import current_app
from flask.ext.script import Manager

from rpress import db
from rpress import create_app


manager = Manager(create_app())


#----------------------------------------------------------------------
@manager.command
def init_db():
    """不能正常工作，可能是当前缺少 model 关联操作"""
##    app.request_context()
##    with app.app_context():
    from rpress.models import Blog
    db.create_all()

    return


#----------------------------------------------------------------------
def main():
    """"""
    manager.run()

    return


if __name__ == "__main__":
    main()