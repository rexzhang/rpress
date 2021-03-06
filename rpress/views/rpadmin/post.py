#!/usr/bin/env python
# coding=utf-8


import re
from datetime import datetime

from sqlalchemy import desc
import flask
from flask import redirect, url_for, flash
from flask_login import login_required, current_user

from rpress.constants import PUBLISH_FSM_DEFINE
from rpress.models import User, Post
from rpress.database import db
from rpress.runtimes.rpadmin.template import render_template, set_navbar
from rpress.runtimes.current_session import get_current_site
from rpress.helpers.validate import is_valid_post_type
from rpress.helpers.fsm_publish import PublishFSM
from rpress.forms import PostEditForm

app = flask.Blueprint('rpadmin_post', __name__)


def flatten(a):
    for each in a:
        if not isinstance(each, list):
            yield each
        else:
            yield from flatten(each)


@app.route('/<string:post_type>/list', methods=['GET'])
@login_required
def list(post_type):
    publish_status_display_list = [
        PUBLISH_FSM_DEFINE.STATE.DRAFT,
        PUBLISH_FSM_DEFINE.STATE.UNPUBLISHED,
        PUBLISH_FSM_DEFINE.STATE.PUBLISHED,
        PUBLISH_FSM_DEFINE.STATE.TRASH
    ]  # for pre-sort
    content = {}

    if not is_valid_post_type(post_type):
        return redirect(url_for('.list', post_type='blog'))

    site = get_current_site()
    queryset = Post.query.filter_by(site=site, type=post_type)

    for publish_status in publish_status_display_list:
        count = queryset.filter_by(publish_status=publish_status).count()
        if count == 0:
            continue

        content[publish_status] = {
            'count': count,
            'list': queryset.filter_by(publish_status=publish_status).order_by(desc('published_time')).all(),
        }

    set_navbar(level1=post_type)
    return render_template(
        "rpadmin/post/list.html", post_type=post_type, content=content
    )


@app.route('/<uuid:post_id>/publish/<string:trigger>', methods=['GET'])
@login_required
def change_publish_status(post_id, trigger):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.name is None or post.content is None:
        flash('can not change publish status!')
        return redirect(url_for('rpadmin_post.edit', post_id=post_id))

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
        post.published_time = datetime.now()
    else:
        post.published = False

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('rpadmin_post.edit', post_id=post_id))


@app.route('/<string:post_type>/new', methods=['GET', ])
@login_required
def new(post_type):
    """"""
    if not is_valid_post_type(post_type):
        return

    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return

    site = get_current_site()

    post = Post(author=user, site=site, type=post_type)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('.edit', post_id=post.id))


@app.route('/<uuid:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
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

    set_navbar(level1=post.type)
    return render_template(
        "rpadmin/post/edit.html", form=form, post=post,
        publish_triggers=post_publish_fsm.possible_triggers
    )
