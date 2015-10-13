#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import re

import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


__all__ = ['configure_filter', ]


_code_block_begin_re = '\[code:[a-z]+\]\n'
_code_block_begin_html = '<pre><code>\n'
_code_block_end_re = '\n\[/code\]'
_code_block_end_html = '\n</code></pre>'

r1 = re.compile('\[code(?P<code>:[a-z]+\]\n[\w\W]+?)\n\[/code\]')
r2 = re.compile('^:(?P<lang>[a-z]+?)\](?P<code>\n[\w\W]+)')
#----------------------------------------------------------------------
def configure_filter(app):
    """"""
    @app.template_filter('datetime2str_short')
    def filter_datatime2str_short(value):
        return value.strftime(format="%Y-%m-%d")

    def filter_codeblock_old(string):
        begin_amount = len(re.findall(_code_block_begin_re, string))
        en_amount = len(re.findall(_code_block_end_re, string))

        string = re.sub(_code_block_begin_re, _code_block_begin_html, string)
        string = re.sub(_code_block_end_re, _code_block_end_html, string)

        if begin_amount > en_amount:
            for x in xrange(begin_amount - en_amount):
                string += _code_block_end_html
        return string

    @app.template_filter('codeblock')
    def filter_codeblock(string):
        str_list = r1.split(string)

        for index, str_x in enumerate(str_list):
            if len(r2.findall(str_x)) == 0:
                continue

            code_block_list = r2.findall(str_x)[0]
            str_list[index] = highlight_code(code_block_list[1], code_block_list[0])

        return ''.join(str_list)

    return


#----------------------------------------------------------------------
def highlight_code(string, lang):
    """"""
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = HtmlFormatter()

    return pygments.highlight(string, lexer, formatter)