#!/usr/bin/env python
# coding=utf-8


import click
from flask.cli import FlaskGroup

from rpress.application import create_app_for_cli
from rpress.commands.develop import click_group as develop


@click.group(cls=FlaskGroup, create_app=create_app_for_cli)
def click_group():
    pass


click_group.add_command(develop, name='develop')


if __name__ == '__main__':
    click_group()
