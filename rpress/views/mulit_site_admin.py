#!/usr/bin/env python
# coding=utf-8


from flask import Blueprint, redirect, url_for
from flask_login import login_required

from rpress.database import db
from rpress.helpers.template.common import render_template
from rpress.models import Site
from rpress.forms import SiteForm


multi_site_admin = Blueprint('multi_site_admin', __name__)


@multi_site_admin.route('', methods=['GET'])
@login_required
def index():
    """mulit-site home page"""
    sites = Site.query.all()

    return render_template('rp/mulit_site_admin/index.html', sites=sites)


@multi_site_admin.route('/new', methods=['GET'])
@login_required
def new():
    """"""
    site = Site(domain='rpress.sample.com')
    db.session.add(site)
    db.session.commit()

    return redirect(url_for('.site_edit', site_id=site.id))


@multi_site_admin.route('/<int:site_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(site_id):
    """"""
    site = Site.query.filter_by(id=site_id).first()
    if site is None:
        return

    form = SiteForm(obj=site)

    if form.validate_on_submit():
        form.populate_obj(site)
        db.session.add(site)
        db.session.commit()
    else:
        pass  # !!!

    return render_template('rp/mulit_site_admin/edit.html', site_id=site_id, form=form)


@multi_site_admin.route('/<int:site_id>/delete', methods=['GET'])
@login_required
def delete(site_id):
    """"""
    print(site_id)  # !!!!!

    return redirect(url_for('.index'))
