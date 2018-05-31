#!/usr/bin/env python
# coding=utf-8


"""
为开发环境生成数据。
"""


import click
from flask.cli import with_appcontext

from rpress import db
from rpress.models import User
from rpress.helpers.data_init import add_site_sample_data, import_data_from_wordpress_xml
from rpress.helpers.prompt import ask_user_name, create_new_user_with_default_password


@click.command()
@with_appcontext
def command():
    db.create_all()
    user_name = 'admin'
    user_password = 'password'
    site_domain_name = '127.0.0.1'

    user = User.query.filter_by(name=user_name).first()
    if user is not None:
        print('duplicate user name!')
        return None

    user = User(name=user_name, password=user_password)
    db.session.add(user)

    add_site_sample_data(db_session=db.session, site_domain=site_domain_name, admin_user=user)
    db.session.commit()
    return


def db_create():
    """create db's schema, create first/admin user
    alembic (0.8.3) can't support sqlite for upgrade:
    (NotImplementedError: No support for ALTER of constraints in SQLite dialect)"""

    db.create_all()

    print('create admin user...')
    user = create_new_user_with_default_password()
    if user is None:
        return

    db.session.add(user)
    db.session.commit()
    return


def db_add_site():
    """create first site, first blog and page; config admin user"""
    from rpress.models import User

    print('create site...')
    site_domain_name = prompt('site domain')

    print('site admin user name...')
    user_name = ask_user_name()
    user = User.query.filter_by(name=user_name).first()
    if user is None:
        user = create_new_user_with_default_password(user_name)
        if user is None:
            print('error!!')
            return

    add_site_sample_data(db_session=db.session, site_domain=site_domain_name, admin_user=user)
    db.session.commit()
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
