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
        summoner = self.lookup_summoner(summoner_name)
        if summoner:
            self.accounts[user] = {}
            self.accounts[user]['summoner_name'] = summoner_name
            self._save_info()
            return True
        else:
            return False


    def _delete_user(self, user):
        if self.account_exists(user):
            del(self.accounts[user])
            self._save_info()


    def _get_summoner(self, user):
        summoner = self.riotapi.get_summoner_by_name(self.accounts[user]['summoner_name'])
        return summoner


    def lookup_summoner(self, name):
        try:
            summoner = self.riotapi.get_summoner_by_name(name)
            return summoner
        except:
            return None
        

    def account_exists(self, user):
        if self.accounts.get(user, None):
            return True
        else:
            return False
    
    
    #TODO summary information
    @commands.command()
    async def summoner_lookup(self, *args):
        summoner_name = ' '.join(args)
        summoner = self.lookup_summoner(summoner_name)

        if summoner:
            await self.bot.say("{} is level {} summoner on the NA server".format(
                summoner.name, summoner.level
            ))
        else:
            await self.bot.say("Unable to find user")


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
    async def associate(self, ctx, *args):
        user = ctx.message.author.id

        if len(args) >= 2:
            if args[0] == '-override':
                self._delete_user(user)
                summoner_name = ' '.join(args[1:])
        else:
            summoner_name = ' '.join(args)


        if self.account_exists(user):
            response = """\
            This account already exists. If you wish to overwrite this do:
            <op>associate -override new name
            """
            await self.bot.say(response)
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
