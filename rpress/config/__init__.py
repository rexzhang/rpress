#!/usr/bin/env python
# coding=utf-8

try:
    from .running import Config  # noqa: F401
except ImportError:
    from .develop import Config  # noqa: F401
