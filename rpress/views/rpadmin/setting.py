#!/usr/bin/env python
# coding=utf-8


import flask
from flask import flash
from flask_login import login_required

from rpress.models import SiteSetting
from rpress.database import db
from rpress.helpers.template.common import render_template
from rpress.helpers.mulit_site import get_current_request_site
from rpress.helpers.site import get_current_request_site_info
from rpress.forms import SettingsForm

app = flask.Blueprint('rpadmin_setting', __name__)


@app.route('/', methods=['GET', ])
@login_required
def list():
    content = {
        'site': get_current_request_site_info(),
    }

    return render_template('rpadmin/setting/list.html', content=content)


@app.route('/<string:key>/edit', methods=['GET', 'POST'])
@login_required
def edit(key):
    """"""
    site = get_current_request_site()
    site_setting = SiteSetting.query.filter_by(site=site, key=key).first()
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

        flash("setting updated", "success")
    else:
        flash('setting edit error')

    return render_template("rpadmin/setting/edit.html", form=form, site_setting=site_setting)
