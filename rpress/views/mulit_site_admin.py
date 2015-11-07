#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from flask import Blueprint, redirect, url_for
from flask.ext.login import login_required

from rpress import db
from rpress.helpers.template.common import render_template
from rpress.models import Site
from rpress.forms import SiteForm


mulit_site_admin = Blueprint('mulit_site_admin', __name__)


@mulit_site_admin.route('', methods=['GET',])
@login_required
#----------------------------------------------------------------------
def index():
    """mulit-site home page"""
    sites = Site.query.all()

    return render_template('rp/mulit_site_admin/index.html', sites=sites)


@mulit_site_admin.route('/new', methods=['GET',])
@login_required
#----------------------------------------------------------------------
def new():
    """"""
    site = Site(name="newsite", domain="new.sample.com")
    db.session.add(site)
    db.session.commit()

    return redirect(url_for('.site_edit', site_id=site.id))


@mulit_site_admin.route('/<int:site_id>/edit', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
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
        pass  #!!!

    return render_template('rp/mulit_site_admin/edit.html', site_id=site_id, form=form)


@mulit_site_admin.route('/<int:site_id>/delete', methods=['GET',])
@login_required
#----------------------------------------------------------------------
def delete(site_id):
    """"""
    print(site_id)  #!!!!!

    return redirect(url_for('.index'))
