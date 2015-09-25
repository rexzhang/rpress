#!/usr/bin/env python
#coding=utf-8


class ConfigDefault(object):
    DEBUG = True


class ConfigDev(ConfigDefault):
    DEBUG = True


class ConfigRelease(ConfigDefault):
    DEBUG = False

