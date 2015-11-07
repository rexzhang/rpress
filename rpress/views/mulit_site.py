#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from flask import Blueprint, redirect, url_for
from flask.ext.login import login_required

from rpress import db
from rpress.helpers.template.common import render_template
from rpress.models import Site
from rpress.forms import SiteForm

mulit_site = Blueprint('mulit_site', __name__)


@mulit_site.route('', methods=['GET',])
@login_required
#----------------------------------------------------------------------
def index():
    """mulit-site home page"""
    sites = Site.query.all()

    return render_template('rp/mulit_site/index.html', sites=sites)


@mulit_site.route('/new', methods=['GET',])
@login_required
#----------------------------------------------------------------------
def site_new():
    """"""
    site = Site(name="newsite", domain="new.sample.com")
    db.session.add(site)
    db.session.commit()

    return redirect(url_for('.site_edit', site_id=site.id))


@mulit_site.route('/<int:site_id>/edit', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
def site_edit(site_id):
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

    return render_template('rp/mulit_site/site_edit.html', site_id=site_id, form=form)


@mulit_site.route('/<int:site_id>/delete', methods=['GET',])
@login_required
#----------------------------------------------------------------------
def site_delete(site_id):
    """"""
    print(site_id)  #!!!!!

    return redirect(url_for('.index'))
