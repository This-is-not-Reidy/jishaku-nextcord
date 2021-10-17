# -*- coding: utf-8 -*-

"""
jishaku
~~~~~~~

A discord.py extension including useful tools for bot development and debugging.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

# pylint: disable=wildcard-import
from jishaku_nextcord.cog import *  # noqa: F401
from jishaku_nextcord.features.baseclass import Feature  # noqa: F401
from jishaku_nextcord.flags import Flags  # noqa: F401
from jishaku_nextcord.meta import *  # noqa: F401

__all__ = (
    'jishaku_nextcord',
    'Feature',
    'Flags',
    'setup'
)
