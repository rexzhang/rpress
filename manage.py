#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import


#from flask import Flask
#from flask import current_app
from flask.ext.script import Manager, prompt_bool, prompt
from flask.ext.migrate import MigrateCommand

from rpress import create_app
from rpress import db
from rpress.helpers.uuid1plus import uuid1fromdatetime
from rpress.helpers.data_init import add_site_sample_data, import_data_from_wordpress_xml
from rpress.helpers.prompt import create_new_user_with_default_password

manager = Manager(create_app(config_name='dev'))  #!!!
manager.add_command('db', MigrateCommand)


@manager.command
#----------------------------------------------------------------------
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


@manager.command
#----------------------------------------------------------------------
def db_add_site():
    """create first site, first blog and page; config admin user"""
    from rpress.models import User

    print('create site...')
    site_domain_name = prompt('site domain')

    user = create_new_user_with_default_password()
    if user is None:
        return

    add_site_sample_data(db_session=db.session, site_domain=site_domain_name, admin_user=user)
    db.session.commit()
    return


@manager.option('-f', '--filename', required=True)
@manager.option('-c', '--disable-convert-code-tag', default=False)
#----------------------------------------------------------------------
def importer(disable_convert_code_tag, filename):
    """"""
    from rpress.models import Site

    site_domain = prompt('site domain')
    site = Site.query.filter_by(domain=site_domain).first()
    if site is None:
        return "[ERROR] invalue site domain!"

    import_data_from_wordpress_xml(db_session=db.session, site=site, disable_convert_code_tag=disable_convert_code_tag, filename=filename)

    #commit
    db.session.commit()
    return


#----------------------------------------------------------------------
def main():
    """"""
    manager.run()

    return


if __name__ == "__main__":
    main()
