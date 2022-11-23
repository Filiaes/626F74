import discord, subprocess
from discord.ext import tasks, commands
import config as cfg

class Status(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.status.start()
        self.index = 0

    def cog_unload(self):
        self.status.cancel()

    @tasks.loop(seconds=60.0)
    async def status(self):
        # getpid = str(os.system("ps -ef | grep bot.py | tr -s ' ' | cut -d ' ' -f2 | head -1"))
        getpid = int(subprocess.check_output("ps -ef | grep bot.py | tr -s ' ' | cut -d ' ' -f2 | head -1", shell=True))
        # print(f"{getpid}")
        pid = str(getpid)
        # print(f"{pid}")
        await self.client.change_presence(activity=discord.Activity(type=cfg.atype, name=pid), status = cfg.status)

    @status.before_loop
    async def before_status(self):
        await self.client.wait_until_ready()

async def setup(client):
    await client.add_cog(Status(client))