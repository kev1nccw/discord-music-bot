from discord.ext import commands

import main.config as config
from main.helpers import permission_check


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.command(name="shutdown", aliases=["restart", "reset"])
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...!")
        _, voice = await permission_check(self.bot, ctx)
        if voice and voice.is_playing():
            voice.stop()
        await self.bot.close()

    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send(config.HELP)
