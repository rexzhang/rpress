#!/usr/bin/env python
# coding=utf-8


import codecs

from pathlib import Path

import click
from flask.cli import with_appcontext

from rpress.models import Site
from rpress.runtimes.data_export_import_v1 import export_site_data_to_json_str, import_site_data_from_json


@click.command()
@with_appcontext
def command_export():
    for site in Site.query:
        json_str, filename = export_site_data_to_json_str(site.id)

        with codecs.open(filename, 'w+', encoding='utf-8') as fp:
            fp.write(json_str)

    return


@click.command()
@with_appcontext
def command_import():
    p = Path('.')
    for filename in p.glob('*.rpress.json'):
        # compatible 3.5
        # TypeError: invalid file: PosixPath
        import_site_data_from_json(str(filename))

    return
