#!/usr/bin/env python
# coding=utf-8


import re

from sqlalchemy import desc
import flask
from flask import redirect, url_for, flash
from flask_login import login_required, current_user

from rpress.constants import PUBLISH_FSM_DEFINE
from rpress.models import User, Post, Term, SiteSetting
from rpress.database import db
from rpress.helpers.template.common import render_template
from rpress.helpers.validate import is_valid_post_type
from rpress.helpers.fsm_publish import PublishFSM
from rpress.helpers.mulit_site import get_current_request_site
from rpress.helpers.site import get_current_request_site_info
from rpress.forms import PostEditForm, TermEditFrom, SettingsForm

site_admin = flask.Blueprint('site_admin', __name__)


@site_admin.route('', methods=['GET'])
@login_required
def index():
    """"""
    return render_template("rp/site_admin/list.html")


@site_admin.route('/term/list/<term_type>', methods=['GET', ])
@login_required
def term_list(term_type):
    """"""
    if term_type not in ['category', 'tag']:
        return  # !!!

    site = get_current_request_site()

    terms = Term.query.filter_by(site=site, type=term_type).order_by(desc('name')).all()
    return render_template('rp/site_admin/term_list.html', terms=terms)


@site_admin.route('/term/<string:name>/edit', methods=['GET', 'POST'])
@login_required
def term_edit(name):
    """"""
    site = get_current_request_site()

    term = Term.query.filter_by(site=site, name=name).first_or_404()  # !!!
    form = TermEditFrom(obj=term)

    if form.validate_on_submit():
        form.populate_obj(term)

        db.session.add(term)
        db.session.commit()

        flash("term updated", "success")
        # return redirect(url_for('.blog'))
    else:
        flash('term edit error')
        pass

    return render_template("rp/site_admin/term_edit.html", form=form, term=term)



