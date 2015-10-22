#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from transitions import Machine


########################################################################
class BaseFSM(object):
    """FSM base class
    please add:

    STATE_XXXX = 'xxxx'
    STATE_YYYY = 'yyyy'

    STATE_DEFAULT = STATE_XXXX

    TRIGGER_XXXX = 'xXxX'

    states = [STATE_XXXX,]
    transitions = [
        {'trigger': TRIGGER_XXXX, 'source': STATE_XXXX, 'dest': STATE_YYYY,},
    ]
    """

    transitions = []
    _triggers = []

    #----------------------------------------------------------------------
    def __init__(self, init_state=None):
        """Constructor"""
        if init_state is None:
            init_state = self.STATE_DEFAULT

        self.m = Machine(model=self, states=self.states, transitions=self.transitions, initial=init_state)
        return

    @property
    #----------------------------------------------------------------------
    def triggers(self):
        """"""
        if len(self._triggers) == 0:
            action_set = set()

            for transition in self.transitions:
                action_set.add(transition['trigger'])
            self._triggers = list(action_set)

        return self._triggers

    @property
    #----------------------------------------------------------------------
    def possible_triggers(self):
        """"""
        triggers = set()
        for transition in self.transitions:
            if self.state in transition['source']:
                triggers.add(transition['trigger'])

        return list(triggers)

    #----------------------------------------------------------------------
    def do_trigger(self, trigger_name):
        """"""
        return self.__dict__[trigger_name](self)


# publish FSM
########################################################################
class PublishFSM(BaseFSM):
    """publish Finite State Machine"""
    STATE_DRAFT = 'draft'
    STATE_PUBLISHED = 'published'
    STATE_UNPUBLISHED = 'unpublished'
    STATE_TRASH = 'trash'
    STATE_HISTORY = 'history'

    STATE_DEFAULT = STATE_DRAFT

    TRIGGER_PUBLISH = 'publish'
    TRIGGER_UNPUBLISH = 'unpublish'
    TRIGGER_DELETE = 'delete'

    states = [STATE_DRAFT, STATE_PUBLISHED, STATE_UNPUBLISHED, STATE_TRASH, STATE_HISTORY]
    transitions = [
        {'trigger': TRIGGER_PUBLISH, 'source': [STATE_DRAFT, STATE_UNPUBLISHED, STATE_TRASH], 'dest': STATE_PUBLISHED,},
        {'trigger': TRIGGER_UNPUBLISH, 'source': STATE_PUBLISHED, 'dest': STATE_UNPUBLISHED,},
        {'trigger': TRIGGER_DELETE, 'source': STATE_PUBLISHED, 'dest': STATE_TRASH,},
    ]
