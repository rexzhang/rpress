#!/usr/bin/env python
#coding=utf-8


from sqlalchemy.orm import scoped_session, sessionmaker

from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
#session = db.session
##session = scoped_session(sessionmaker(autocommit=False, autoflush=False, #bind=engine))
##                                      bind=db))

