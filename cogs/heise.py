import feedparser, dateparser, os, sys
from discord.ext import tasks, commands
import config as cfg

path = "./data"
logf = "./data/heise"

class Heise(commands.Cog):
    def __init__(self, client):
        self.index = 0
        self.client = client
        self.parser.start()

    def cog_unload(self):
        self.parser.cancel()

    @tasks.loop(seconds=300.0)
    async def parser(self):
        feed = feedparser.parse('https://www.heise.de/security/rss/news-atom.xml')
        if os.path.isfile(logf) and os.path.exists(path):
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

        elif os.path.exists(path):
            with open(logf, 'w') as f:
                for entry in feed.entries:
                    timestamp = int(dateparser.parse(entry["published"]).timestamp())
                    f.write(f"{timestamp}" + '\n')
        else:
            os.makedirs(path)
            with open(logf, 'w') as f:
                for entry in feed.entries:
                    timestamp = int(dateparser.parse(entry["published"]).timestamp())
                    f.write(f"{timestamp}" + '\n')
    
    @parser.before_loop
    async def before_parser(self):
        await self.client.wait_until_ready()

async def send_feed(client, flink, channel_id):
    channel = client.get_channel(channel_id)
    await channel.send(flink)

async def setup(client):
    await client.add_cog(Heise(client))