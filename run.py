import discord
from discord import Activity, ActivityType
from discord.ext import commands

import main.config as config
from main.commands.admin import Admin
from main.commands.music import Music

bot = commands.Bot(command_prefix=config.BOT_PREFIX, help_command=None)

if __name__ == "__main__":
    if config.BOT_TOKEN == "":
        print(config.BOT_TOKEN_NOT_FOUND)
        exit

    bot.add_cog(Music(bot))
    bot.add_cog(Admin(bot))


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=Activity(name=config.READY_STATUS, type=ActivityType.listening),
    )
    print(config.ON_READY)


bot.run(config.BOT_TOKEN)
