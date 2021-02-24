from discord.ext import commands
from discord import Embed, TextChannel, VoiceChannel
from typing import Union, Optional

from src.utils.loader import load

items = load("./data/resources.yml")
res = items["resources"]
aliases = items["aliases"]


class Random(commands.Cog):
    """A set of random commands for Soren"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.files = {}

    def resolve(self, items: dict):
        out = {}

        for name, value in items.items():
            if isinstance(value, str) and value.startswith("$$"):
                filename = "./data" + value[2:]
                if filename in self.files:
                    out[name] = self.files[filename]
                else:
                    with open(filename) as f:
                        data = f.read()
                        self.files[filename] = data
                        out[name] = data
            else:
                out[name] = value

        return out

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

        await ctx.send(embed=Embed(
            title=f"{icon} {channel.name}",
            description=description,
        ))

    @commands.command(name="resource", aliases=["r"])
    async def res(self, ctx: commands.Context, name: str):
        if name in aliases:
            name = aliases[name]

        if name not in res:
            return await ctx.send("Resource not found.")

        config = res[name]

        embed = None
        content = None
        if "embed" in config:
            data = self.resolve(config["embed"])
            embed = Embed(**data)
        else:
            content = self.resolve(config["text"])["content"]

        await ctx.send(content=content, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Random(bot))