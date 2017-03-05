import discord
import aiohttp

from os import getenv
from discord.ext import commands
from json import loads, dumps
from bs4 import BeautifulSoup

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

        if len(create_data["options"]) < 2:
            await self.bot.say("2 Options is the minimum required options")
            return

        if create_data["title"].lower() == "help":
            await self.bot.say("<op> title;option1;option2;...")
            return
        
        async with aiohttp.post(create_poll_url, data = dumps(create_data)) as response:
            if response.status != 200:
                await self.bot.say("Error making this poll")
                return

            holding = await response.json()

            await self.bot.say("Here's a link to the poll: {}".format(
                strawpoll + str(holding["id"])
            ))

    
    @commands.command()
    async def subreddit_preview(self, subreddit : str):
        """Gets current top 3 and top 3 all time for reddit"""
        url = 'https://www.reddit.com'

        try:
            import praw
        except:
            await self.bot.say("Error: Please contact admin")
            return


        reddit = praw.Reddit(
            client_id=getenv('reddit_client_id'),
            client_secret=getenv('reddit_client_secret'),
            password=getenv('reddit_password'),
            user_agent=getenv('reddit_user_agent'),
            username=getenv('reddit_username')
        )

        try:
            subreddit = reddit.subreddit(subreddit)

            hot_posts = []
            top_posts = []

            for submission in subreddit.hot(limit=10):
                if len(hot_posts) == 3:
                    break
                elif submission.stickied:
                    continue
                else:
                    hot_posts.append(url + submission.permalink)

            for submission in subreddit.top('all', limit=10):
                if len(top_posts) == 3:
                    break
                elif submission.stickied:
                    continue
                else:
                    top_posts.append(url + submission.permalink)

            response = """
            Subreddit : {}

            Hot Posts Now: 
            1. {}
            2. {}
            3. {}

            Top Posts All Time:
            1. {}
            2. {}
            3. {}
            """.format(
                subreddit,
                hot_posts[0], hot_posts[1], hot_posts[2],
                top_posts[0], top_posts[1], top_posts[2]
            )

            await self.bot.say(response)

        except:
            await self.bot.say("Error with subreddit. Either doesn't exist or error connecting to reddit")
            return


def setup(bot):
    bot.add_cog(Utility(bot))
