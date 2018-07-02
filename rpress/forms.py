#!/usr/bin/env python
# coding=utf-8


from wtforms import StringField, TextAreaField, PasswordField
from wtforms import validators, SubmitField
from flask_wtf import FlaskForm as Form


class LoginForm(Form):
    username = StringField('用户', [validators.Length(min=3, max=50)])
    password = PasswordField('密码', [validators.Length(min=8)])
    submit = SubmitField('登陆')


class PostEditForm(Form):
    title = StringField('标题', [validators.Length(min=4, max=128)])
    name = StringField('name', [validators.Length(min=0, max=128)])
    content = TextAreaField('正文', [validators.Length(min=4)])
    submit = SubmitField("submit")


class ProfilesForm(Form):
    """"""
    email = StringField('电子邮箱', [validators.Email()])
    display = StringField('显示名字')
    submit = SubmitField("submit")


class PasswordForm(Form):
    """"""
    password_old = StringField('当前密码')
    password_new = StringField('新密码')
    submit = SubmitField("submit")


class SiteForm(Form):
    """"""
    domain = StringField('网站域名')
    submit = SubmitField("submit")


class SettingsForm(Form):
    """"""
    value = StringField('value')

    submit = SubmitField("submit")


class TermEditFrom(Form):
    """"""
    name = StringField('名字')
    desc = StringField('描述')
    submit = SubmitField("submit")
