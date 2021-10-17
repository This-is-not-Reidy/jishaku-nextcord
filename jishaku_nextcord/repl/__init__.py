# -*- coding: utf-8 -*-

"""
jishaku_nextcord.repl
~~~~~~~~~~~~

Repl-related operations and tools for jishaku_nextcord.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

# pylint: disable=wildcard-import
from jishaku_nextcord.repl.compilation import *  # noqa: F401
from jishaku_nextcord.repl.disassembly import disassemble  # noqa: F401
from jishaku_nextcord.repl.inspections import all_inspections  # noqa: F401
from jishaku_nextcord.repl.repl_builtins import get_var_dict_from_ctx  # noqa: F401
from jishaku_nextcord.repl.scope import *  # noqa: F401
