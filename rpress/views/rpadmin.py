#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import re

from sqlalchemy import desc
import flask
from flask import g, request, redirect, url_for, flash
from flask.ext.login import login_required, current_user

from rpress import db
from rpress.helpers.template.common import render_template
from rpress.helpers.validate import is_valid_post_type
from rpress.helpers.fsm import PublishFSM
from rpress.helpers.mulit_site import get_current_request_site
from rpress.models import User, Site, Post, Term, SiteSetting
from rpress.forms import PostEditForm, ProfilesForm, PasswordForm, SiteForm, TermEditFrom


rpadmin = flask.Blueprint('rpadmin', __name__)


@rpadmin.route('/', methods=['GET'])
@login_required
#----------------------------------------------------------------------
def index():
    """"""
    return render_template("/rpadmin/index.html")


@rpadmin.route('/post/list/<string:type>', methods=['GET'])
@login_required
#----------------------------------------------------------------------
def post_list(type):
    """"""
    if not is_valid_post_type(type):
        return  #!!!

    site = get_current_request_site()

    posts = Post.query.filter_by(site=site, type=type).order_by(desc('publish_date')).all()

    return render_template("/rpadmin/post_list.html", posts=posts, post_type=type)


@rpadmin.route('/post/<uuid:uuid>/publish/<string:trigger>', methods=['GET'])
@login_required
#----------------------------------------------------------------------
def post_publish_state(uuid, trigger):
    """"""
    post = Post.query.filter_by(uuid=str(uuid)).first_or_404()  #!!!
    if post.publish_state not in PublishFSM.states:
        return  #!!!

    post_publish_fsm = PublishFSM(init_state=post.publish_state)
    if trigger not in post_publish_fsm.triggers:
        return  #!!!

    if not post_publish_fsm.do_trigger(trigger_name=trigger):
        return  #!!!

    print('Done......')
    post.publish_state = post_publish_fsm.state
    if post_publish_fsm.state == PublishFSM.STATE_PUBLISHED:
        post.published = True
    else:
        post.published = False

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('rpadmin.post_edit', uuid=uuid))


@rpadmin.route('/post/<uuid:uuid>/edit', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
def post_edit(uuid):
    """"""
    post = Post.query.filter_by(uuid=str(uuid)).first_or_404()  #!!!
    form = PostEditForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        post.content = re.sub(r'\r', '\n', re.sub(r'\r\n', '\n', form.data['content']))

        db.session.add(post)
        db.session.commit()

        flash("post updated", "success")
        #return redirect(url_for('.blog'))
    else:
        flash('post edit error')
        pass

    post_publish_fsm = PublishFSM(post.publish_state)
    return render_template("/rpadmin/post_edit.html", form=form, post=post, publish_actions=post_publish_fsm.possible_triggers)


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

    site = get_current_request_site()

    post = Post(author=user, site=site)
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


#----------------------------------------------------------------------
def _make_site_settings_info(site):
    """"""
    SITE_SETTINGS_KEY_LIST = ['title', 'desc']

    site_settings = {}

    for key in SITE_SETTINGS_KEY_LIST:
        site_setting = SiteSetting.query.filter_by(site=site, key=key).first()

        site_settings[key] = site_setting.value

    return site_settings


@rpadmin.route('/site', methods=['GET',])
@login_required
#----------------------------------------------------------------------
def site():
    """"""
    site = Site.query.filter_by(id=1).first()
    if site is None:
        return

    content = {
        'site': site,
        'site_settings': _make_site_settings_info(site),
    }

    return render_template('rpadmin/site.html', content=content)


@rpadmin.route('/term/list/<string:type>', methods=['GET', ])
@login_required
#----------------------------------------------------------------------
def term_list(type):
    """"""
    if type not in ['category', 'tag']:
        return  #!!!

    site = get_current_request_site()

    terms = Term.query.filter_by(site=site, type=type).order_by(desc('name')).all()
    return render_template('rpadmin/term_list.html', terms=terms)


@rpadmin.route('/term/<string:name>/edit', methods=['GET', 'POST'])
@login_required
#----------------------------------------------------------------------
def term_edit(name):
    """"""
    site = get_current_request_site()

    term = Term.query.filter_by(site=site, name=name).first_or_404()  #!!!
    form = TermEditFrom(obj=term)

    if form.validate_on_submit():
        form.populate_obj(term)

        db.session.add(term)
        db.session.commit()

        flash("term updated", "success")
        #return redirect(url_for('.blog'))
    else:
        flash('term edit error')
        pass

    return render_template("/rpadmin/term_edit.html", form=form, term=term)
