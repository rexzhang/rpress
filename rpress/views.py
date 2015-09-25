#!/usr/bin/env python
#coding=utf-8


from flask import Blueprint
from flask.views import MethodView


instance = Blueprint('index',__name__)

class TestView(MethodView):
    def get(self):
        return 'hello world'

instance.add_url_rule('/test',view_func=TestView.as_view('test'),methods=['GET',])
