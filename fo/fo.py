import discord
import aiohttp
import os

from discord.ext import commands
from json import loads, dumps
from cogs.utils.dataIO import dataIO
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy

ENDPOINT = 'https://www.foaas.com'

class Fo:
    """League Related Cog. Not that expansive."""

    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(pass_context=True)
    async def fo(self, ctx, to_user : discord.User):
        from_name = str(ctx.message.author).split('#')[0]
        to_name = to_user.name
        return_url = ENDPOINT + '/off/{}/{}'.format(to_name, from_name)
        await self.bot.say(to_user.mention + " This is for you: {}".format(return_url))


def setup(bot):
    bot.add_cog(Fo(bot))
