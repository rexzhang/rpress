#!/usr/bin/env python
# coding=utf-8


from pathlib import Path

import click
from flask.cli import with_appcontext

from rpress.models import Site
from rpress.runtimes.data_export_import_v1 import export_site_data_to_json, import_site_data_from_json


@click.command()
@with_appcontext
def command_export():
    for site in Site.query:
        export_site_data_to_json(site.id)

    return


@click.command()
@with_appcontext
def command_import():
    p = Path('.')
    for filename in p.glob('*.rpress.json'):
        import_site_data_from_json(filename)

    return
