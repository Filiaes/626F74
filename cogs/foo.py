from discord.ext import commands
import config as cfg

class FooMsg(commands.Cog):
    def __init__(self, client):
        self.client = client
""" 
        @client.command()
        async def foo(ctx):
            channel = client.get_channel(1039145875852755004)
            await channel.send('Welcome,' + '\n' + '\n' + 'you are probably here because you need some help with a service hosted by filiaes. Please reload the channel you have joined, if you find yourself unable to write. The role assignment needs a couple of seconds. Feel free to ask your questions afterwards.')
"""
async def setup(client):
    await client.add_cog(FooMsg(client))