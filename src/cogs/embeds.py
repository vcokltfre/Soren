from discord.ext import commands
from discord import Embed, File
from json import loads, dumps
from io import StringIO


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

    @commands.command(name="extract")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.channel)
    async def status(self, ctx: commands.Context, *, link: str):
        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        cid, mid = link.split("-")

        try:
            channel = self.bot.get_channel(int(cid))
            message = await channel.fetch_message(int(mid))
        except:
            return await ctx.send("Invalid message link.")

        if not message.embeds:
            return await ctx.send("Message has no embeds.")

        embed = message.embeds[0]
        embed = embed.to_dict()

        data = dumps(embed, indent=2)

        if len(data) + 50 < 2000:
            return await ctx.send(f"Embed source:\n```json\n{data}```")

        data = StringIO(data)

        await ctx.send(content="Embed source:", file=File(data, "extracted.json"))


def setup(bot: commands.Bot):
    bot.add_cog(Embeds(bot))