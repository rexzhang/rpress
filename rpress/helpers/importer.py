#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import


import re


#----------------------------------------------------------------------
def convert_code_tag(string):
    """
    convert code tag:
    [language_name]xxx[/language_name] to:
    [code:language_name]xxx[/code]
    """
    code_name_list = list(set(re.findall('\[/([a-z]+?)\]', string)))
    #print('found code name:%r' % code_name_list)

    for code_name in code_name_list:
        string = re.sub('\[%s\]\n' % code_name, '[code:%s]\n' % code_name, string)
        string = re.sub('\n\[/%s\]' % code_name, '\n[/code]', string)

    return string