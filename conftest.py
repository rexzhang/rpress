#!/usr/bin/env python
# coding=utf-8


import pytest
from rpress.application import create_app_for_testing


@pytest.fixture
def app():
    return create_app_for_testing()
