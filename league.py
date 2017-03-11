import discord
import aiohttp
import os

from discord.ext import commands
from json import loads, dumps
from cogs.utils.dataIO import dataIO
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy

"""
TODOS:
Want to add timed strawpoll?

"""
file_path = 'data/league/accounts.json'
endpoint = 'https://na.api.pvp.net/api/lol/na/'


class League:
    """League Related Cog. Not that expansive."""

    def __init__(self, bot):
        self.accounts = dataIO.load_json(file_path)
        self.riotapi = riotapi
        self.riotapi.set_api_key(os.getenv("riot_api_key"))
        self.riotapi.set_region("NA")
        self.riotapi.set_load_policy(LoadPolicy.lazy)
        self.bot = bot
        

    def _save_info(self):
        dataIO.save_json(file_path, self.accounts)


    def _create_user(self, user, summoner_name):
        summoner = self.riotapi.get_summoner_by_name(summoner_name)
        if summoner:
            self.accounts[user] = {}
            self.accounts[user]['summoner_name'] = summoner_name
            self._save_info()
            return True
        else:
            return False


    def _get_summoner(self, user):
        summoner = self.riotapi.get_summoner_by_name(self.accounts[user]['summoner_name'])
        return summoner
        

    def account_exists(self, user):
        if self.accounts.get(user, None):
            return True
        else:
            return False
    
    
    # TODO
    @commands.command(pass_context=True)
    async def last_match(self, ctx):
        endpoint = "http://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/"
        user = ctx.message.author.id
        if self.account_exists(user):
            summoner = self._get_summoner(user)
            game_list = self.riotapi.get_recent_games(summoner)
            last_game = game_list[0]
            await self.bot.say("Heres your last match: {}".format(endpoint + str(last_game.id) + 
                "?tab=overview"))
            return
        else:
            await self.bot.say("Please associate an account")
            return


    @commands.command(pass_context=True)
    async def associate(self, ctx, summoner_name : str):
        user = ctx.message.author.id
        if self.account_exists(user):
            await self.bot.say("Account already exists")
            return

        if self._create_user(user, summoner_name):
            await self.bot.say("Success")
            return
        else:
            await self.bot.say("Failure associating accounts.")
            return


def setup(bot):
    if not os.path.exists("data/league"):
        os.makedirs("data/league")
    if not os.path.exists(file_path):
        dataIO.save_json(file_path, {})
    bot.add_cog(League(bot))
