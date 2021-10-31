# -*- coding: utf-8 -*-

"""
jishaku_nextcord.features.root_command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The jishaku_nextcord root command.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import math
import sys
import typing

import nextcord
from nextcord.ext import commands

import jishaku_nextcord
from jishaku_nextcord.features.baseclass import Feature
from jishaku_nextcord.flags import Flags
from jishaku_nextcord.modules import package_version
from jishaku_nextcord.paginators import PaginatorInterface

try:
    import psutil
except ImportError:
    psutil = None


def natural_size(size_in_bytes: int):
    """
    Converts a number of bytes to an appropriately-scaled unit
    E.g.:
        1024 -> 1.00 KiB
        12345678 -> 11.77 MiB
    """
    units = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

    power = int(math.log(size_in_bytes, 1024))

    return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"


class RootCommand(Feature):
    """
    Feature containing the root jsk command
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jsk.hidden = Flags.HIDE

    @Feature.Command(name="jishaku_nextcord", aliases=["jsk"],
                     invoke_without_command=True, ignore_extra=False)
    async def jsk(self, ctx: commands.Context):  # pylint: disable=too-many-branches
        """
        The jishaku_nextcord debug and diagnostic commands.

        This command on its own gives a status brief.
        All other functionality is within its subcommands.
        """

        summary = [
            f"jishaku_nextcord **{jishaku_nextcord.__version__}**, nextcord **{nextcord.__version__}**, "
            f"Python **{sys.version}** on **{sys.platform}**".replace("\n", ""),
            f"Модуль загружен: <t:{self.start_time.timestamp():.0f}:R>.",
            ""
        ]

        # detect if [procinfo] feature is installed

        cache_summary = f"Stats: **{len(self.bot.guilds)} guild(s) and {len(self.bot.users)} user(s).**"

        if nextcord.version_info >= (1, 5, 0):
            presence_intent = f"**presence** intent is {'**enabled**' if self.bot.intents.presences else '**disabled**'}"
            members_intent = f"**members** intent is {'**enabled**' if self.bot.intents.members else '**disabled**'}"
            message_intent = f"**messages** intent is {'**enabled**' if self.bot.intents.messages else '**disabled**'}"

            summary.append(f"{message_cache}, {presence_intent} and {members_intent}, and {message_intent}.")
        else:
            guild_subscriptions = f"guild subscriptions are {'enabled' if self.bot._connection.guild_subscriptions else 'disabled'}"

            summary.append(f"{message_cache} and {guild_subscriptions}.")

        # pylint: enable=protected-access

        # Show websocket latency in milliseconds
        summary.append(f"Ping: **{round(self.bot.latency * 1000, 2)} ms**")

        await ctx.send("\n".join(summary))

    # pylint: disable=no-member
    @Feature.Command(parent="jsk", name="hide")
    async def jsk_hide(self, ctx: commands.Context):
        """
        Hides jishaku_nextcord from the help command.
        """

        if self.jsk.hidden:
            return await ctx.send("jishaku_nextcord is already hidden.")

        self.jsk.hidden = True
        await ctx.send("jishaku_nextcord is now hidden.")

    @Feature.Command(parent="jsk", name="show")
    async def jsk_show(self, ctx: commands.Context):
        """
        Shows jishaku_nextcord in the help command.
        """

        if not self.jsk.hidden:
            return await ctx.send("jishaku_nextcord is already visible.")

        self.jsk.hidden = False
        await ctx.send("jishaku_nextcord is now visible.")
    # pylint: enable=no-member

    @Feature.Command(parent="jsk", name="tasks")
    async def jsk_tasks(self, ctx: commands.Context):
        """
        Shows the currently running jishaku_nextcord tasks.
        """

        if not self.tasks:
            return await ctx.send("No currently running tasks.")

        paginator = commands.Paginator(max_size=1985)

        for task in self.tasks:
            paginator.add_line(f"{task.index}: `{task.ctx.command.qualified_name}`, invoked at "
                               f"{task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
        return await interface.send_to(ctx)

    @Feature.Command(parent="jsk", name="cancel")
    async def jsk_cancel(self, ctx: commands.Context, *, index: typing.Union[int, str]):
        """
        Cancels a task with the given index.

        If the index passed is -1, will cancel the last task instead.
        """

        if not self.tasks:
            return await ctx.send("No tasks to cancel.")

        if index == "~":
            task_count = len(self.tasks)

            for task in self.tasks:
                task.task.cancel()

            self.tasks.clear()

            return await ctx.send(f"Cancelled {task_count} tasks.")

        if isinstance(index, str):
            raise commands.BadArgument('Literal for "index" not recognized.')

        if index == -1:
            task = self.tasks.pop()
        else:
            task = nextcord.utils.get(self.tasks, index=index)
            if task:
                self.tasks.remove(task)
            else:
                return await ctx.send("Unknown task.")

        task.task.cancel()
        return await ctx.send(f"Cancelled task {task.index}: `{task.ctx.command.qualified_name}`,"
                              f" invoked at {task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")
