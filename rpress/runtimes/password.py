#!/usr/bin/env python
# coding=utf-8


import hashlib


def generate_password_hash(password):
    return hashlib.sha256(bytes(password, 'utf8')).hexdigest()  # TODO salt


def check_password_hash(password, hashed_password):
    if password is not None and hashlib.sha256(bytes(password, 'utf8')).hexdigest() == hashed_password:
        return True

    return False
