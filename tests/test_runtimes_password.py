#!/usr/bin/env python
# coding=utf-8


import flask_testing

from rpress.runtimes.password import generate_password_hash, check_password_hash
from rpress.application import create_app_for_testing
from rpress.database import db


class TestRuntimePassword(flask_testing.TestCase):
    def create_app(self):
        self.db = db
        self.app = create_app_for_testing()
        return self.app

    def tet_password(self):
        password_list = ['abc', 123]

        for password in password_list:
            self.assertEqual(
                check_password_hash(hashed_password=generate_password_hash(password=password), password=password), True
            )
        return
