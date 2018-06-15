#!/usr/bin/env python
# coding=utf-8


class POST(object):
    class TYPE(object):
        BLOG = 'blog'
        PAGE = 'page'


class TERM(object):
    class TYPE(object):
        CATEGORY = 'category'
        TAG = 'tag'


class PUBLISH_FSM_DEFINE(object):
    """publish FSM define"""

    class STATE(object):
        DRAFT = 'draft'
        PUBLISHED = 'published'
        UNPUBLISHED = 'unpublished'
        TRASH = 'trash'
        HISTORY = 'history'

    class TRIGGER(object):
        PUBLISH = 'publish'
        UNPUBLISH = 'unpublish'
        DELETE = 'delete'

    DEFAULT_STATE = STATE.DRAFT
    transitions = [
        {'trigger': TRIGGER.PUBLISH, 'source': [STATE.DRAFT, STATE.UNPUBLISHED, STATE.TRASH],
         'dest': STATE.PUBLISHED, },
        {'trigger': TRIGGER.UNPUBLISH, 'source': STATE.PUBLISHED, 'dest': STATE.UNPUBLISHED, },
        {'trigger': TRIGGER.DELETE, 'source': STATE.PUBLISHED, 'dest': STATE.TRASH, },
    ]


SITE_SETTINGS_KEY_LIST = [
    'title',
    'desc',
    'theme',
    'google_analytics',
    'disqus',
]
