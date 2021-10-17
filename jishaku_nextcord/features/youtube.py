# -*- coding: utf-8 -*-

"""
jishaku_nextcord.features.youtube
~~~~~~~~~~~~~~~~~~~~~~~~~

The jishaku_nextcord youtube-dl command.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import nextcord
import youtube_dl
from nextcord.ext import commands

from jishaku_nextcord.features.baseclass import Feature
from jishaku_nextcord.features.voice import VoiceFeature

BASIC_OPTS = {
    'format': 'webm[abr>0]/bestaudio/best',
    'prefer_ffmpeg': True,
    'quiet': True
}


class BasicYouTubeDLSource(nextcord.FFmpegPCMAudio):
    """
    Basic audio source for youtube_dl-compatible URLs.
    """

    def __init__(self, url, download: bool = False):
        ytdl = youtube_dl.YoutubeDL(BASIC_OPTS)
        info = ytdl.extract_info(url, download=download)
        super().__init__(info['url'])


class YouTubeFeature(Feature):
    """
    Feature containing the youtube-dl command
    """

    @Feature.Command(parent="jsk_voice", name="youtube_dl", aliases=["youtubedl", "ytdl", "yt"])
    async def jsk_vc_youtube_dl(self, ctx: commands.Context, *, url: str):
        """
        Plays audio from youtube_dl-compatible sources.
        """

        if await VoiceFeature.connected_check(ctx):
            return

        if not youtube_dl:
            return await ctx.send("youtube_dl is not installed.")

        voice = ctx.guild.voice_client

        if voice.is_playing():
            voice.stop()

        # remove embed maskers if present
        url = url.lstrip("<").rstrip(">")

        voice.play(nextcord.PCMVolumeTransformer(BasicYouTubeDLSource(url)))
        await ctx.send(f"Playing in {voice.channel.name}.")
