import feedparser
import discord
from discord.ext import commands
import config as cfg

feed = feedparser.parse('https://www.heise.de/security/rss/news-atom.xml')
pointer = feed.entries[1]

class Rss(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rss(self, ctx):
        print (pointer.summary)
        print (pointer.link)
        embed = discord.Embed(title=pointer.summary, url=pointer.link,color = discord.Colour.dark_teal())
        # embed.add_field(name="undefined", value="undefined", inline=False)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Rss(client))