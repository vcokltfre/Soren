All Intents:
```py
import discord
from discord.ext import commands

intents = discord.Intents.all() #Activates all intents including Member and Presence intents.

bot = commands.Bot(command_prefix=' . ', intents=intents, activity = discord.Game('I Added all intents!'))

bot.run(token)
```

Default Intents:
```py
import discord
from discord.ext import commands

intents = discord.Intents.default() #Activates all but member and presence intents

intents.members = True # Subscribes to privileged members intent. Needed to track guild member count, find members, etc.

bot = commands.Bot(command_prefix=' . ', intents=intents, activity= discord.Game('I Added all but presence intents!'))

bot.run(token)
```