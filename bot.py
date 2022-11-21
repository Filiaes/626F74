#!/usr/bin/env python

import discord, os, sys
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found - quit.")
else:
    import config as cfg

intents = discord.Intents.default()
intents.message_content = True

class Client(commands.Bot):
    if cfg.activity:
        def __init__(self):
            super().__init__(
                command_prefix = cfg.prefix,
                intents = intents,
                help_command = commands.DefaultHelpCommand(dm_help=True),
                activity = discord.Activity(name=cfg.aname, type=cfg.atype),
                status = cfg.status
            )
    else:
        def __init__(self):
            super().__init__(
                command_prefix = cfg.prefix,
                intents = intents,
                help_command = commands.DefaultHelpCommand(dm_help=True),
                status = cfg.status
            )        
    
    async def setup_hook(self):
        print(f"\033[31mLogged in as {client.user}\033[39m")
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.tree.sync()
        print("Loaded cogs")
        print(f'discord.py version ({discord.__version__})')

client = Client()
client.run(cfg.token)