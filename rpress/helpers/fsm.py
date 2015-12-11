#!/usr/bin/env python
#coding=utf-8


"""
https://gist.github.com/rexzhang/fc799f97ba3087eac17f
"""


from __future__ import print_function, unicode_literals, absolute_import

from transitions import Machine


########################################################################
class FSM(object):
    """FSM base class
    self.state # current FSM status
    self.is_STATE_NAME # bool
    self.to_STATE_NAME # true to STATE
    """
    DEFAULT_STATE = None

    states = []
    transitions = []

    _triggers = []
    _define_class = None

    #----------------------------------------------------------------------
    def __init__(self, init_state=None, define_class=None):
        """Constructor"""
        if define_class is not None:
            self._define_class = define_class

        self.__parse_fsm_define_data__()

        if init_state is None:
            init_state = self.DEFAULT_STATE

        self.m = Machine(model=self, states=self.states, transitions=self.transitions, initial=init_state)
        return

    #----------------------------------------------------------------------
    def __parse_fsm_define_data__(self):
        """"""
        self.DEFAULT_STATE = self._define_class.DEFAULT_STATE

        for attr_name in  (dir(self._define_class.STATE)):
            if '__' in attr_name:
                continue

            self.states.append(getattr(self._define_class.STATE, attr_name))

        self.transitions = self._define_class.transitions
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
