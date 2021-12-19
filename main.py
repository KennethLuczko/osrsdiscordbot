import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# ----- THEATER OF BLOOD
@bot.command(name='tob', help='Returns the loot from Theater of Blood.')
async def tob(tob):
    tob_loot = [
        'Scythe of Vitur',
        'Sanguinesti Staff',
        "Justicar Helmet"
    ]
    response = random.choice(tob_loot)
    await tob.send(response)

# ----- CHAMBERS OF XERIC
@bot.command(name='cox', help='Returns the loot from Chambers of Xeric.')
async def cox(cox):
    cox_loot = [
        'Twisted Bow',
        'Kodai Insignia',
        "Dexterous Prayer Scroll"
    ]

    response = random.choice(cox_loot)
    await cox.send(response)

bot.run(TOKEN)