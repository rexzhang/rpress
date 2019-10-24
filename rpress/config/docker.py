#!/usr/bin/env python
# coding=utf-8


from .release import Config as ConfigBase

db_settings = {
    'HOST': 'host.docker.internal',
    'PORT': ConfigBase.SQLALCHEMY_DATABASE['PORT'],
    'NAME': ConfigBase.SQLALCHEMY_DATABASE['NAME'],
    'USER': ConfigBase.SQLALCHEMY_DATABASE['USER'],
    'PASSWORD': ConfigBase.SQLALCHEMY_DATABASE['PASSWORD'],
}

try:
    from .settings import DB_SETTINGS

    for k in db_settings:
        v = DB_SETTINGS.get(k)
        if v:
            db_settings[k] = v

except ImportError:
    pass


class Config(ConfigBase):
    ConfigBase.SQLALCHEMY_DATABASE['HOST'] = db_settings['HOST']
    ConfigBase.SQLALCHEMY_DATABASE['PORT'] = db_settings['PORT']
    ConfigBase.SQLALCHEMY_DATABASE['NAME'] = db_settings['NAME']
    ConfigBase.SQLALCHEMY_DATABASE['USER'] = db_settings['USER']
    ConfigBase.SQLALCHEMY_DATABASE['PASSWORD'] = db_settings['PASSWORD']
