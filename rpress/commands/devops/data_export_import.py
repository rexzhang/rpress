#!/usr/bin/env python
# coding=utf-8


import click
from flask.cli import with_appcontext

from rpress.runtimes.data_export_import_v1 import export_site_data_to_json


@click.command()
@with_appcontext
def command_export():
    site_id = 1
    export_site_data_to_json(int(site_id))
    return
