#!/usr/bin/env python
#coding=utf-8


from wtforms import BooleanField, StringField, TextField, TextAreaField, PasswordField
from wtforms import validators, SubmitField
from flask.ext.wtf import Form


class LoginForm(Form):
    username = StringField(u'用户', [validators.Length(min=3)])
    password = PasswordField(u'密码', [validators.Length(min=8)])
    submit = SubmitField(u'登陆')


class PostEditForm(Form):
    title = StringField(u'标题', [validators.Length(min=4)])
    name = StringField(u'name', [validators.Length(min=4)])
    content = TextAreaField(u'正文', [validators.Length(min=4)])
    submit = SubmitField("submit")
