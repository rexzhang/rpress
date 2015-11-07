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
from rpress.helpers.data_init import add_site_sample_data, import_site_from_wordpress


manager = Manager(create_app(config_name='dev'))  #!!!
manager.add_command('db', MigrateCommand)


@manager.command
#----------------------------------------------------------------------
def db_create():
    """create db's schema, create first/admin user
    alembic (0.8.3) can't support sqlite for upgrade:
    (NotImplementedError: No support for ALTER of constraints in SQLite dialect)"""
    #如果不能正常工作，可能是当前缺少 model 关联操作
    from rpress.models import User

    db.create_all()

    admin_user_name = prompt('user(admin) name')
    user = User(name=admin_user_name, password='password')

    db.session.add(user)
    db.session.commit()
    return

@manager.command
#----------------------------------------------------------------------
def db_add_site():
    """create first site, first blog and page, admin user"""
    from rpress.models import User

    site_name = prompt('site name')
    site_domain = prompt('site domain')
    admin_user_name = prompt('user(admin) name')

    admin_user = User.query.filter_by(name=admin_user_name).first()

    add_site_sample_data(db_session=db.session, site_name=site_name, site_domain=site_domain, admin_user=admin_user)
    db.session.commit()
    return


@manager.option('-f', '--filename', required=True)
@manager.option('-c', '--disable-convert-code-tag', default=False)
#----------------------------------------------------------------------
def importer(disable_convert_code_tag, filename):
    """"""
    from rpress.models import Site

    site_domain = prompt('site domain')
    site = Site.query.filter_by(domain=site_domain).first()  #!!!!!!!!!!!!!!!!

    import_site_from_wordpress(db_session=db.session, site=site, disable_convert_code_tag=disable_convert_code_tag, filename=filename)

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
