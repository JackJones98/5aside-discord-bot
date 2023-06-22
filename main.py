"""
Driver file for the discord bot
"""
# ============================================================
import os

TOKEN = os.environ.get('token')
path = os.environ.get('path')
channel_key = os.environ.get('channel')

print(os.listdir('data/'))
print(TOKEN, path, channel_key)
# path = '//TRUENAS/Misc_storage/5aside_discord_bot/'
# TOKEN = open("//TRUENAS/Misc_storage/env_vars/discord.txt", "r").read()
# channel_key = 'test'

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ------------------------------------------------------------
# load meta data 
import json
with open(f'{path}meta_data.json', 'r') as f:
    meta = json.load(f)

# process meta data
channels = meta['channel_id']
channel_id = channels[channel_key]
admin = meta['admin_id'][0]

# ------------------------------------------------------------

from matches.games import Fixtures
from general_fns import general_msg, user_help, AdminCmd, Scheduler
from user_data_mgt.team import Team

# ============================================================
# Instantiate classes

def intialise(channel):
    "Instantiate classes"

    fixtures = Fixtures(bot, path, channel) # fixtures class
    team = Team(bot, fixtures, path, channel) # team/user data

    scheduler = Scheduler(bot, meta, path, team, fixtures) # scheduler

    admin = AdminCmd(bot, team, fixtures, scheduler) # admin commands

    return fixtures, team, admin


@bot.event
async def on_ready():
    # ------------------------------------------------------
    # Start up messages
    print(f'{bot.user} has connected to Discord!')

    gen_channel = bot.get_channel(462411915839275009)

    #test_channel = bot.get_channel(1112672147412893696)
    channel = bot.get_channel(channel_id)

    # ------------------------------------------------------
    # Instantiate classes
    fixtures, team, admin = intialise(channel)

    await bot.add_cog(fixtures)
    await bot.add_cog(team)

    # admin commands
    await bot.add_cog(admin)

    admin.general_debug()



user_help(bot)
general_msg(bot)


bot.run(TOKEN)