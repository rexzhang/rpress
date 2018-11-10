#!/usr/bin/env python
# coding=utf-8
from flask import request
from flask_login import current_user

from rpress.models import Site
from rpress.helpers.site import get_site_settings


def get_current_user_info():
    """current session user info"""
    if not current_user.is_active:
        return None

    return {
        'id': current_user.id,
        'name': current_user.name,
    }


def get_current_site_domain():
    """current request site domain, like rexzhang.com"""
    return request.environ['HTTP_HOST'].split(':')[0]


def get_current_request_site():
    """current site object for current request"""
    domain = get_current_site_domain()

    site = Site.query.filter_by(domain=domain).first()
    if site is None:
        site = Site.query.order_by('created_time').first()

    return site


def get_current_site_info():
    """current session site info"""
    site = get_current_request_site()  # TODO: redis cache site info
    if site is None:
        return None

    return {
        'id': site.id,
        'domain': site.domain,
        'settings': get_site_settings(site),  # TODO: maybe remove it?
    }
