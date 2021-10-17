# -*- coding: utf-8 -*-

"""
jishaku_nextcord.cog
~~~~~~~~~~~~

The jishaku_nextcord debugging and diagnostics cog implementation.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands

from jishaku_nextcord.features.filesystem import FilesystemFeature
from jishaku_nextcord.features.guild import GuildFeature
from jishaku_nextcord.features.invocation import InvocationFeature
from jishaku_nextcord.features.management import ManagementFeature
from jishaku_nextcord.features.python import PythonFeature
from jishaku_nextcord.features.root_command import RootCommand
from jishaku_nextcord.features.shell import ShellFeature
from jishaku_nextcord.features.voice import VoiceFeature

__all__ = (
    "JishakuNextcord",
    "STANDARD_FEATURES",
    "OPTIONAL_FEATURES",
    "setup",
)

STANDARD_FEATURES = (VoiceFeature, GuildFeature, FilesystemFeature, InvocationFeature, ShellFeature, PythonFeature, ManagementFeature, RootCommand)

OPTIONAL_FEATURES = []

try:
    from jishaku_nextcord.features.youtube import YouTubeFeature
except ImportError:
    pass
else:
    OPTIONAL_FEATURES.insert(0, YouTubeFeature)


class JishakuNextcord(*OPTIONAL_FEATURES, *STANDARD_FEATURES):  # pylint: disable=too-few-public-methods
    """
    The frontend subclass that mixes in to form the final jishaku_nextcord cog.
    """


def setup(bot: commands.Bot):
    """
    The setup function defining the jishaku_nextcord.cog and jishaku_nextcord extensions.
    """

    bot.add_cog(jishaku_nextcord(bot=bot))
