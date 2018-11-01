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
    return render_template("rp/site_admin/index.html")


@site_admin.route('/post/list/<post_type>', methods=['GET'])
@login_required
def post_list(post_type):
    """"""
    if not is_valid_post_type(post_type):
        return  # !!!

    site = get_current_request_site()

    posts = Post.query.filter_by(site=site, type=post_type).order_by(desc('published_time')).all()

    return render_template("rp/site_admin/post_list.html", posts=posts, post_type=post_type)


@site_admin.route('/post/<uuid:post_id>/publish/<string:trigger>', methods=['GET'])
@login_required
def post_publish_status(post_id, trigger):
    """"""
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.name is None or post.content is None:
        return redirect(url_for('site_admin.post_edit', post_id=post_id))

    if post.publish_status not in PublishFSM.states:
        return

    post_publish_fsm = PublishFSM(init_state=post.publish_status)
    if trigger not in post_publish_fsm.triggers:
        return

    if not post_publish_fsm.do_trigger(trigger_name=trigger):
        return

    post.publish_status = post_publish_fsm.state
    if post_publish_fsm.state == PUBLISH_FSM_DEFINE.STATE.PUBLISHED:
        post.published = True
    else:
        post.published = False

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('site_admin.post_edit', post_id=post_id))


@site_admin.route('/post/<post_type>/new', methods=['GET', ])
@login_required
def post_new(post_type):
    """"""
    if not is_valid_post_type(post_type):
        return

    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return

    site = get_current_request_site()

    post = Post(author=user, site=site, type=post_type)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('.post_edit', post_id=post.id))


@site_admin.route('/post/<uuid:post_id>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    """"""
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostEditForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        post.content = re.sub(r'\r', '\n', re.sub(r'\r\n', '\n', form.data['content']))

        db.session.add(post)
        db.session.commit()

        flash("post updated", "success")
        # return redirect(url_for('.blog'))
    else:
        flash('post edit error')
        pass

    post_publish_fsm = PublishFSM(init_state=post.publish_status)
    return render_template("rp/site_admin/post_edit.html", form=form, post=post,
                           publish_triggers=post_publish_fsm.possible_triggers)


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


@site_admin.route('/settings', methods=['GET', ])
@login_required
def settings():
    """"""
    content = {
        'site': get_current_request_site_info(),
    }

    return render_template('rp/site_admin/settings.html', content=content)


@site_admin.route('/setting/<string:key>/edit', methods=['GET', 'POST'])
@login_required
def setting_edit(key):
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

    return render_template("rp/site_admin/setting_edit.html", form=form, site_setting=site_setting)
