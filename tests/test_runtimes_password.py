#!/usr/bin/env python
# coding=utf-8


import flask_testing

from rpress.application import create_app_for_testing
from rpress.database import db


class TestRuntimePassword(flask_testing.TestCase):
    def create_app(self):
        self.db = db
        self.app = create_app_for_testing()
        return self.app

    def test_demo(self):
        return
