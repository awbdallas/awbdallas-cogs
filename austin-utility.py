import discord
import aiohttp

from discord.ext import commands
from json import loads, dumps

"""
TODOS:
Want to add timed strawpoll?

"""

class Utility:
    """Cog for small utility functions on my server"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def strawpoll(self, command : str):
        """Makes a straw poll"""
        create_poll_url = 'https://strawpoll.me/api/v2/polls'
        strawpoll = 'https://www.strawpoll.me/'

        create_data = {
            "title" : command.split(';')[0],
            "options" : command.split(';')[1:],
            "multi": True
        }

        
        async with aiohttp.post(create_poll_url, data = dumps(create_data)) as response:
            if response.status != 200:
                await self.bot.say("Error making this poll")
                return

            holding = await response.json()

            await self.bot.say("Here's a link to the poll: {}".format(
                strawpoll + str(holding["id"])
            ))


def setup(bot):
    bot.add_cog(Utility(bot))
