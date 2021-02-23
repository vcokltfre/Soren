from discord.ext import commands
from discord import Embed
from json import loads


class Embeds(commands.Cog):
    """Embed commands for Soren"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def strip_cb(text: str):
        if text.startswith("```"):
            until = text.find("\n")
            text = text[until:]

        if text.endswith("```"):
            text = text[:-3]

        return text

    @commands.command(name="embed")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
    async def status(self, ctx: commands.Context, *, text: str):
        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        await ctx.send(embed=Embed.from_dict(loads(self.strip_cb(text))))


def setup(bot: commands.Bot):
    bot.add_cog(Embeds(bot))