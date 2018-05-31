#!/usr/bin/env python
# coding=utf-8


"""
为开发环境生成数据。
"""


import click
from flask.cli import with_appcontext

from rpress import db
from rpress.helpers.data_init import import_data_from_wordpress_xml
from rpress.runtimes.fake_data import add_sample_user_and_site


@click.command()
@with_appcontext
def command():
    db.create_all()
    add_sample_user_and_site(
        user_name='admin',
        user_password='password',
        site_domain_name='127.0.0.1'
    )

    return


# @manager.option('-f', '--filename', required=True)
# @manager.option('-c', '--disable-convert-code-tag', default=False)
def importer(disable_convert_code_tag, filename):
    """"""
    from rpress.models import Site

    site_domain = prompt('site domain')
    site = Site.query.filter_by(domain=site_domain).first()
    if site is None:
        return "[ERROR] invalid site domain!"

    import_data_from_wordpress_xml(db_session=db.session, site=site, disable_convert_code_tag=disable_convert_code_tag, filename=filename)

    #commit
    db.session.commit()
    return
