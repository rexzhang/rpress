#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from sqlalchemy import desc
import flask
from flask import g, request, redirect, url_for, flash
from flask.ext.login import login_required, current_user

from rpress import db
from rpress.helpers.template import render_template
from rpress.helpers.validate import is_valid_post_type
from rpress.models import Post, User
from rpress.forms import PostEditForm, ProfilesForm, PasswordForm


rpadmin = flask.Blueprint('rpadmin', __name__)


@rpadmin.route('/', methods=['GET'])
@login_required
#----------------------------------------------------------------------
def index():
    """"""
    return render_template("/rpadmin/index.html")


@rpadmin.route('/post/<string:type>/list', methods=['GET'])
@login_required
#----------------------------------------------------------------------
def post_list(type):
    """"""
    if not is_valid_post_type(type):
        return  #!!!

    posts = Post.query.filter_by(type=type).order_by(desc('create_date')).all()

    return render_template("/rpadmin/post_list.html", posts=posts, post_type=type)


@rpadmin.route('/post/<uuid:uuid>/publish/turn', methods=['GET'])
@login_required
#----------------------------------------------------------------------
def post_publish_status_turn(uuid):
    """"""
    post = Post.query.filter_by(uuid=str(uuid)).first_or_404()  #!!!
    if post.publish == True:
        post.publish = False
        post.publish_ext = 'draft'
    else:
        post.publish = True
        post.publish_ext = 'publish'

    db.session.add(post)
    db.session.commit()

    next = request.args.get('next')  #!!!
    return redirect(next or url_for('.index'))


@rpadmin.route('/post/<uuid:uuid>/edit', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
def post_edit(uuid):
    """"""
    post = Post.query.filter_by(uuid=str(uuid)).first_or_404()  #!!!
    form = PostEditForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()

        flash("post updated", "success")
        #return redirect(url_for('.blog'))
    else:
        flash('post edit error')
        pass

    return render_template("/rpadmin/post_edit.html", uuid=str(uuid), form=form)


@rpadmin.route('/post/<string:type>/new', methods=['GET',])
@login_required
#----------------------------------------------------------------------
def post_new(type):
    """"""
    if not is_valid_post_type(type):
        return  #!!!

    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return  #!!!

    post = Post(user)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('.post_edit', uuid=post.uuid))


@rpadmin.route('/profiles', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
def profiles():
    """"""
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return  #!!!
    form = ProfilesForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
    else:
        pass  #!!!

    return render_template('rpadmin/profiles.html', form=form)


@rpadmin.route('/profiles/password', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
def profiles_password():
    """"""
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return  #!!!

    form = PasswordForm()

    if form.validate_on_submit():
        if user.password_validate(form.data['password_old']):
            user.password = form.data['password_new']

            db.session.add(user)
            db.session.commit()

            flash('password is changed!')
            return redirect(url_for('rpadmin.profiles'))

        else:
            flash("old password is NOT correct")

    else:
        pass  #!!!

    return render_template('rpadmin/profiles_password.html', form=form)