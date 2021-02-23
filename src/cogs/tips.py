from discord.ext import commands
from discord import Embed
from re import compile

og = compile(r"og:[a-z]+")
content = compile(r"content=\"[^\"]+\"")


class Tips(commands.Cog):
    """Get tips from the d.py bot tutorial"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="tip")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    async def tip(self, ctx: commands.Context, name: str):
        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

        resp = await self.bot.httpclient.request("GET", f"https://vcokltfre.dev/tips/{name}")

        if resp.status >= 400:
            return await ctx.send("No tip was found by that name!")

        text = await resp.text()
        text = text.replace("><", "\n")
        lines = text.split("\n")

        title = None
        description = None
        url = None
        image = None

        for line in lines:
            if t := og.search(line):
                t = t.group().split(":")[1]
                c = content.search(line).group()[9:-1]

                if t == "title":
                    title = c
                elif t == "description":
                    description = c
                elif t == "url":
                    url = c
                elif t == "image":
                    image = c

        embed = Embed(title=title, description=description, colour=0x87ceeb, url=url)
        if image: embed.set_image(url=image)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Tips(bot))