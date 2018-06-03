#!/usr/bin/env python
# coding=utf-8


from wtforms import StringField, TextAreaField, PasswordField
from wtforms import validators, SubmitField
from flask_wtf import FlaskForm as Form


class LoginForm(Form):
    username = StringField(u'用户', [validators.Length(min=3, max=50)])
    password = PasswordField(u'密码', [validators.Length(min=8)])
    submit = SubmitField(u'登陆')


class PostEditForm(Form):
    title = StringField(u'标题', [validators.Length(min=4, max=128)])
    name = StringField(u'name', [validators.Length(min=0, max=128)])
    content = TextAreaField(u'正文', [validators.Length(min=4)])
    submit = SubmitField("submit")


class ProfilesForm(Form):
    """"""
    email = StringField(u'电子邮箱', [validators.Email()])
    display = StringField(u'显示名字')
    submit = SubmitField("submit")


class PasswordForm(Form):
    """"""
    password_old = StringField(u'当前密码')
    password_new = StringField(u'新密码')
    submit = SubmitField("submit")


class SiteForm(Form):
    """"""
    domain = StringField(u'网站域名')
    submit = SubmitField("submit")


class SettingsForm(Form):
    """"""
    value = StringField(u'value')

    submit = SubmitField("submit")


class TermEditFrom(Form):
    """"""
    name = StringField(u'名字')
    desc = StringField(u'描述')
    submit = SubmitField("submit")
