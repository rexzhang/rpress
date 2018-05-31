#!/usr/bin/env python
# coding=utf-8


from .base import ConfigBase


class Config(ConfigBase):
    # Deploy
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False

    # Session/Cookie/Flask-Login
    SECRET_KEY = "THIS IS SECRET KEY, PLEASE CHANGE FOR PRODUCT ENVIRONMENT"
