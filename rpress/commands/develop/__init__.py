#!/usr/bin/env python
# coding=utf-8


import click

from . import init


@click.group()
def click_group():
    """development tools"""
    pass


click_group.add_command(init.command, name='init')
