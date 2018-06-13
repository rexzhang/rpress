#!/usr/bin/env python
# coding=utf-8


import click
from flask.cli import FlaskGroup

from rpress.application import create_app_for_cli
from rpress.commands.develop import click_group as develop
from rpress.commands.devops import click_group as devops


@click.group(cls=FlaskGroup, create_app=create_app_for_cli)
def click_group():
    pass


click_group.add_command(develop, name='develop')
click_group.add_command(devops, name='devops')


if __name__ == '__main__':
    click_group()
