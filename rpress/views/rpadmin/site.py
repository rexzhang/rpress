#!/usr/bin/env python
# coding=utf-8


from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required

from rpress.database import db
from rpress.runtimes.rpadmin.template import render_template, navbar
from rpress.models import Site
from rpress.forms import SiteForm


app = Blueprint('rpadmin_site', __name__)


@app.route('', methods=['GET'])
@login_required
@navbar(level1='sites')
def list():
    """mulit-site home page"""
    sites = Site.query.all()

    return render_template('rpadmin/site/list.html', sites=sites)


@app.route('/new', methods=['GET'])
@login_required
def new():
    """"""
    site = Site(domain='rpress.sample.com')
    db.session.add(site)
    db.session.commit()

    return redirect(url_for('.edit', site_id=site.id))


@app.route('/<uuid:site_id>/edit', methods=['GET', 'POST'])
@login_required
@navbar(level1='sites')
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

    return render_template('rpadmin/site/edit.html', site_id=site_id, form=form)


@app.route('/<uuid:site_id>/delete', methods=['GET'])
@login_required
def delete(site_id):
    """"""
    print(site_id)  # !!!!!
    flash('delete site:{}, skip...'.format(site_id))

    return redirect(url_for('.list'))
