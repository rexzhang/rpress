#!/usr/bin/env python
#coding=utf-8


import os


basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigDefault(object):
    DEBUG = True
    THEME_DEFAULT = 'rexzhangname'
    SECRET_KEY = 'this is secret key, please change for product environment'


class ConfigDev(ConfigDefault):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'rpress_dev.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_ECHO = True


class ConfigRelease(ConfigDefault):
    DEBUG = False

