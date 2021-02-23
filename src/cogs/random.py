from discord.ext import commands
from discord import Embed, TextChannel, VoiceChannel
from typing import Union, Optional


class Random(commands.Cog):
    """A set of random commands for Soren"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ce")
    async def channelembed(self, ctx: commands.Context, channel: Optional[Union[TextChannel, VoiceChannel]]):
        channel = channel or ctx.channel
        description = None
        if isinstance(channel, VoiceChannel):
            icon = ":loud_sound:"
        else:
            icon = ":hash:"
            if channel.topic:
                description = channel.topic

        await ctx.send(Embed(
            title=f"{icon} {channel.name}",
            description=description,
        ))


def setup(bot: commands.Bot):
    bot.add_cog(Random(bot))