#!/usr/bin/env python
# coding=utf-8


from .base import ConfigBase


class Config(ConfigBase):
    # Deploy
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

    ConfigBase.SQLALCHEMY_DATABASE['NAME'] = 'rpress_develop'
