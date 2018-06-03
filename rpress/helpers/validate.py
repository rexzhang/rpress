#!/usr/bin/env python
# coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import


def is_valid_post_type(post_type):
    """"""
    if post_type in ['blog', 'page']:
        return True

    return False
