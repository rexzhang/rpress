#!/usr/bin/env python
# coding=utf-8


from .develop import Config as ConfigBase


class Config(ConfigBase):
    SQLALCHEMY_DATABASE_URI = 'postgresql://rpress:xxx@host.docker.internal/rpress_0_x?client_encoding=utf8'
