#!/usr/bin/env python
# coding=utf-8


import flask
from flask import flash
from flask_login import login_required

from rpress.models import SiteSetting
from rpress.database import db
from rpress.runtimes.rpadmin.template import render_template, navbar
from rpress.runtimes.current_session import get_current_site, get_current_site_info
from rpress.forms import SettingsForm

app = flask.Blueprint('rpadmin_setting', __name__)


@app.route('/', methods=['GET', ])
@login_required
@navbar(level1='settings')
def list():
    content = {
        'site': get_current_site_info(),
    }

    return render_template('rpadmin/settings/list.html', content=content)


@app.route('/<string:key>/edit', methods=['GET', 'POST'])
@login_required
@navbar(level1='settings')
def edit(key):
    site = get_current_site()
    site_setting = SiteSetting.query.filter_by(site=site, key=key).order_by('created_time').first()
    if site_setting is None:
        site_setting = SiteSetting(
            site_id=site.id,
            key=key,
            value=None,
        )

    form = SettingsForm(obj=site_setting)

    if form.validate_on_submit():
        form.populate_obj(site_setting)

        db.session.add(site_setting)
        db.session.commit()

        flash("settings updated", "success")
    else:
        flash('settings edit error')

    return render_template("rpadmin/settings/edit.html", form=form, site_setting=site_setting)
