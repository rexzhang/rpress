#!/usr/bin/env python
# coding=utf-8


from .develop import Config as ConfigBase


class Config(ConfigBase):
    ConfigBase.SQLALCHEMY_DATABASE['HOST'] = 'host.docker.internal'
