#!/usr/bin/env python
# coding=utf-8


import click

from . import data_export_import


@click.group()
def click_group():
    """DevOps tools"""
    pass


click_group.add_command(data_export_import.command_export, name='export')
click_group.add_command(data_export_import.command_import, name='import')
