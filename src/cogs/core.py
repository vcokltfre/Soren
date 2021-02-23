from discord.ext import commands
from discord import Embed
from datetime import datetime
from time import time
from fractions import gcd


class Core(commands.Cog):
    """A set of core commands for Soren"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.emojis = bot.config.get("emoji", {})
        self.online = self.emojis.get("online", "")
        self.offline = self.emojis.get("offline", "")

    @commands.command(name="status")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.channel)
    async def status(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        uptime = datetime.utcnow() - self.bot.started_at
        latency = f"{round(self.bot.latency * 1000, 2)}ms"

        start = time()
        message = await ctx.send("Timing ping...")
        end = time()

        ping = f"{round((end - start) * 1000, 2)}ms"

        embed = Embed(title="Soren Bot Status", colour=0x87ceeb, timestamp=datetime.utcnow())
        embed.set_author(name="Soren", icon_url=self.bot.user.avatar_url, url="https://vcokltfre.dev")
        embed.description = f"Bot Status: {self.online}\n"
        embed.description += f"API Latency: {ping} / "
        embed.description += f"Gateway Latency: {latency}\n"
        embed.description += f"Uptime: {uptime}\n\n"
        embed.description += f"Message Cache Size: {len(self.bot.cached_messages)}"
        embed.set_footer(text="Creator: vcokltfre#6868", icon_url="https://cdn.discordapp.com/avatars/297045071457681409/a_d8ef3293d06f044af5a70ea7848d5fed.gif")

        await message.edit(embed=embed, content="")

    @commands.command(name="bpr")
    async def bpr(self, ctx: commands.Context):
        bots = len([m for m in ctx.guild.members if m.bot])
        users = ctx.guild.member_count - bots

        cd = gcd(bots, users)

        bots_r, users_r = bots // cd, users // cd

        await ctx.send(f"Bot to person ratio: {bots_r}:{users_r}\nBots: {bots}\nPeople: {users}")


def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))