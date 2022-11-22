import feedparser, dateparser, os, sys
from discord.ext import tasks, commands
import config as cfg

feed = feedparser.parse('https://www.heise.de/security/rss/news-atom.xml')
logf = "./rss_data"

class Rss(commands.Cog):
    def __init__(self, client):
        self.index = 0
        self.client = client
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=60.0)
    async def printer(self):
        if os.path.isfile("./rss_data"):
            data = []
            with open(logf, "r") as f:
                for line in f:
                    x = line[:-1]
                    data.append(x)
                data = [int(i) for i in data]

            for entry in feed.entries:
                title = entry.title
                link = entry.link
                timestamp = int(dateparser.parse(entry["published"]).timestamp())
                if timestamp not in data:
                    message_log_id = cfg.rss_heisesec
                    await send_feed(self.client, link, channel_id=message_log_id)

            with open(logf, 'w') as f:
                for entry in feed.entries:
                    timestamp = int(dateparser.parse(entry["published"]).timestamp())
                    f.write(f"{timestamp}" + '\n')

        else:
            with open(logf, 'w') as f:
                for entry in feed.entries:
                    timestamp = int(dateparser.parse(entry["published"]).timestamp())
                    f.write(f"{timestamp}" + '\n')
    
    @printer.before_loop
    async def before_printer(self):
        await self.client.wait_until_ready()

async def send_feed(client, flink, channel_id):
    channel = client.get_channel(channel_id)
    await channel.send(flink)

async def setup(client):
    await client.add_cog(Rss(client))