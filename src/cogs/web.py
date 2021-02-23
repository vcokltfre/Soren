from discord.ext import commands
from discord import Embed
from datetime import datetime
from re import compile

from src.utils.og import get_og_embed

og = compile(r"og:[a-z]+")
content = compile(r"content=\"[^\"]+\"")


class Web(commands.Cog):
    """Web commands for Soren"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_og(self, url: str):
        resp = await self.bot.httpclient.request("GET", url)

        if resp.status >= 400:
            return None

        text = await resp.text()

        embed = get_og_embed(text)
        embed.colour = 0x87ceeb
        embed.timestamp = datetime.utcnow()

        return embed

    @commands.command(name="tip")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    async def tip(self, ctx: commands.Context, name: str):
        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        embed = await self.get_og(f"https://vcokltfre.dev/tips/{name}")

        if not embed:
            return await ctx.send("That's not a valid tip!")

        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=embed)

    @commands.command(name="getog")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    async def tip(self, ctx: commands.Context, url: str):
        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        if url[0] == "<":
            url = url[1:-1]

        embed = await self.get_og(url)

        if not embed:
            return await ctx.send("That's not a valid URL!")

        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Web(bot))