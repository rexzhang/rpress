#!/usr/bin/env python
# coding=utf-8


from .fsm import FSM
from rpress.constants import PUBLISH_FSM_DEFINE


class PublishFSM(FSM):
    """
    publish Finite State Machine

    state string's length must less than 20, more info check file:models.py
    """

    _define_class = PUBLISH_FSM_DEFINE
