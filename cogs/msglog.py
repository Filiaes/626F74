import discord
from discord.ext import commands
import config as cfg

class MsgLog(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def log_message(self, message, type, before=None, attachments_old=None):
        # Prevent logger from logging itself
        if message.author.id == self.client.user.id:
            return 0

        # Prevent logger from logging DM
        if message.guild is None:
            return 0

        # Check message author
        bot_user = ""
        if message.author.bot:
            bot_user = " (bot)"

        # Check for attachments in the message
        # Discord for desktop and web do not have the ability to send
        # multiple images within the same message. However, this is
        # possible on the mobile versions of discord and through bots.
        try:
            attachments = ""
            count = 1
            for a in message.attachments:
                attachments += f"\n[attachment{count}]({a.url})"
                count += 1
        except Exception:
            attachments = ""

        # Action dependent
        description = ""
        if type == 'Edited':
            color = 0xFAA61A
            description = f"Before:\n{before.content}{attachments_old}\n\nAfter:\n"
        elif type == 'Deleted':
            color = 0xF04747
        elif type == 'Sent':
            color = 0xE3E5E8

        # Create embed
        embed = discord.Embed(title=f"{message.author}{bot_user}",
                              description=f"{description}{message.content}{attachments}\n"
                              f"[jump to message]({message.jump_url})",
                              color=color)
        embed.set_footer(text=f"Author ID: {message.author.id}\nMessage ID: {message.id}")
        embed.set_thumbnail(url=message.author.avatar)
        embed.set_author(name=f"Message {type} in #{message.channel}",
                         icon_url=self.client.user.avatar)

        # Send message to log channel
        message_log_id = cfg.logs
        await send_to_log(self.client, embed, channel_id=message_log_id)

    # Log all messages (debugging)
    if cfg.logall:
        @commands.Cog.listener()
        async def on_message(self, message):
            await self.log_message(message, type='Sent')

    @commands.Cog.listener()
    async def on_message_edit(self, before, message):
        # This event is triggered when an embed is added or removed
        # from a message
        if before.content == message.content:
            return 0

        # Check for any attachments in the old message. The new message
        # will be checked in log_message()
        try:
            attachments_old = ""
            count = 1
            for a in before.attachments:
                attachments_old += f"\n[attachment{count}]({a.url})"
                count += 1
        except Exception:
            attachments_old = ""

        await self.log_message(message, type='Edited', before=before,
                               attachments_old=attachments_old)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.log_message(message, type='Deleted')

async def send_to_log(client, embed, channel_id):
    channel = client.get_channel(channel_id)
    await channel.send(embed=embed)

async def setup(client):
    await client.add_cog(MsgLog(client))