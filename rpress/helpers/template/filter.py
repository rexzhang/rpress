#!/usr/bin/env python
# coding=utf-8


import re

import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


__all__ = ['configure_filter', ]


_code_block_begin_re = '\[code:[a-z]+\]\n'
_code_block_begin_html = '<pre><code>\n'
_code_block_end_re = '\n\[/code\]'
_code_block_end_html = '\n</code></pre>'

r1 = re.compile(r'\[code(?P<code>:[a-z]+\]\n[\w\W]+?)\n\[/code\]')
r2 = re.compile(r'^:(?P<lang>[a-z]+?)\](?P<code>\n[\w\W]+)')

re_html_block = re.compile(r'(?P<html_block>\n<[a-z]+>\n.+\n</[a-z]+>)', flags=re.S)


def configure_filter(app):
    """"""
    @app.template_filter('datetime2str_short')
    def datetime2str_short(value):
        if value is None:
            return str(None)

        return value.strftime(format="%Y-%m-%d")

    def filter_codeblock_old(string):
        begin_amount = len(re.findall(_code_block_begin_re, string))
        en_amount = len(re.findall(_code_block_end_re, string))

        string = re.sub(_code_block_begin_re, _code_block_begin_html, string)
        string = re.sub(_code_block_end_re, _code_block_end_html, string)

        if begin_amount > en_amount:
            for x in range(begin_amount - en_amount):
                string += _code_block_end_html
        return string

    @app.template_filter('post_content')
    def post_content(string):
        str_list = r1.split(string)
        for index, str_x in enumerate(str_list):
            if len(r2.findall(str_x)) == 0:
                # text area
                str_list[index] = text_area(str_x)

            else:
                # code_block
                code_block_list = r2.findall(str_x)[0]
                str_list[index] = code_area_highlight(code_block_list[1], code_block_list[0])

        return ''.join(str_list)

    return


def code_area_highlight(string, lang):
    """"""
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = HtmlFormatter()

    return pygments.highlight(string, lexer, formatter)


def text_area(string):
    """"""
    str_list = re_html_block.split(string)
    for index, str_x in enumerate(str_list):
        if len(re_html_block.findall(str_x)) == 0:
            # text
            str_list[index] = re.sub('\n', '<br>', re.sub('\n+', '\n', str_x))
        else:
            # html_block
            pass

    return ''.join(str_list)
