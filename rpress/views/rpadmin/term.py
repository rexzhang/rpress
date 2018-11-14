#!/usr/bin/env python
# coding=utf-8


from sqlalchemy import desc
import flask
from flask import g, flash
from flask_login import login_required

from rpress.models import Term
from rpress.database import db
from rpress.runtimes.rpadmin.template import render_template, set_navbar
from rpress.runtimes.current_session import get_current_site
from rpress.forms import TermEditFrom

app = flask.Blueprint('rpadmin_term', __name__)


@app.route('/<string:term_type>/list', methods=['GET', ])
@login_required
def list(term_type):
    if term_type not in ['category', 'tag']:
        return  # !!!

    site = get_current_site()

    terms = Term.query.filter_by(site=site, type=term_type).order_by(desc('name')).all()

    set_navbar(level1=term_type)
    return render_template(
        'rpadmin/term/list.html',
        terms=terms, term_type=term_type
    )


@app.route('/<string:term_type>/new', methods=['GET', ])
@login_required
def new(term_type):
    return


@app.route('/<string:name>/edit', methods=['GET', 'POST'])
@login_required
def edit(name):
    site = get_current_site()

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

    set_navbar(level1=term.type)
    return render_template("rpadmin/term/edit.html", form=form, term=term)
