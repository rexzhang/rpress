#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import flask
from flask import request, redirect, url_for, flash
from flask.ext.login import login_required

from rpress import db
from rpress.helpers.template import render_template
from rpress.models import Post, User
from rpress.forms import PostEditForm


rpadmin = flask.Blueprint('rpadmin', __name__)


@rpadmin.route('/', methods=['GET'])
@login_required
#----------------------------------------------------------------------
def index():
    """"""
    return 'this is rPress admin home page'


@rpadmin.route('/rpadmin/<int:post_id>', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
def post_edit(post_id):
    """"""
    post = Post.query.filter_by(id=post_id).first_or_404()  #!!!
    form = PostEditForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()

        #flash(_("Posting success"), "success")
        #return redirect(url_for('.blog'))
    else:
        pass

    return render_template("post_edit.html", post_id=post_id, form=form)
