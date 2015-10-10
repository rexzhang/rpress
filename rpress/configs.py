#!/usr/bin/env python
#coding=utf-8


import os
import ConfigParser


basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigDefault(object):
    DEBUG = False
    THEME_DEFAULT = 'rexzhangname'
    SECRET_KEY = 'this is secret key, please change for product environment'

    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class ConfigDev(ConfigDefault):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'rpress_dev.db')
    #SQLALCHEMY_ECHO = True


########################################################################
class ConfigRelease(ConfigDefault):
    """"""
    DEBUG = False

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        config = ConfigParser.ConfigParser()
        config_filename = os.path.join(basedir, 'deploy.ini')

        if len(config.read(config_filename)) == 0:
            raise "can't read [%s], please check it" % config_filename

        self.SQLALCHEMY_DATABASE_URI = config.get('db', 'SQLALCHEMY_DATABASE_URI')
