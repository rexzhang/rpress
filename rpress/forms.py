#!/usr/bin/env python
#coding=utf-8


from wtforms import BooleanField, StringField, validators, SubmitField
from flask.ext.wtf import Form


class LoginForm(Form):
    username = StringField(u'用户', [validators.Length(min=3)])
    password = StringField(u'密码', [validators.Length(min=4)])
    submit = SubmitField(u'登陆')


class PostEditForm(Form):
    title = StringField(u'标题', [validators.Length(min=4)])
    content = StringField(u'正文', [validators.Length(min=4)])
    submit = SubmitField("submit")
