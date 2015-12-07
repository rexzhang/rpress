#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import os
import ConfigParser


basedir = os.path.abspath(os.path.dirname(__file__))


#----------------------------------------------------------------------
def get_config_obj(name):
    """get config with name"""
    config = None

    if name is None or name == 'dev':
        config = ConfigDev()

    elif name == 'dev_mysql':
        config = ConfigDevMySQL()

    elif name == 'release':
        config = ConfigRelease()

    else:
        raise Exception('unknow config name!')

    return config


class ConfigDefault(object):
    DEBUG = False
    THEME_DEFAULT = 'rexzhangname'
    SECRET_KEY = 'this is secret key, please change for product environment'

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = ''
    #SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class ConfigDev(ConfigDefault):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'rpress.sqlite3')
    #SQLALCHEMY_ECHO = True


########################################################################
class ConfigDevMySQL(ConfigDev):
    """"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/rpress?charset=utf8'


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
            raise Exception("can't read [%s], please check it" % config_filename)

        self.SECRET_KEY = config.get('common', 'SECRET_KEY')
        self.SQLALCHEMY_DATABASE_URI = config.get('db', 'SQLALCHEMY_DATABASE_URI')

        return
