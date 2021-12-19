import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# ----- THEATER OF BLOOD
@bot.command(name='tob', help='Returns the loot from Theater of Blood.')
async def tob(tob, arg):
    if isinstance(int(arg), int):
        scythes = 0
        rapiers = 0
        staves = 0
        faceguards = 0
        chestguards = 0
        legguards = 0
        hilts = 0
        cabbages = 0
        for i in range(0, int(arg)+1):
            diceroll = random.uniform(0, 173)
            if diceroll <= 1:
                scythes += 1
            elif diceroll <= 2:
                rapiers += 1
            elif diceroll <= 4:
                staves += 1
            elif diceroll <= 6:
                faceguards += 1
            elif diceroll <= 8:
                chestguards += 1
            elif diceroll <= 10:
                legguards += 1    
            elif diceroll <= 21:
                hilts += 1
            else:
                cabbages += 1
        response = "Cabbages: " + str(cabbages) + "\n"
        response += "Hilts: " + str(hilts) + "\n"
        response += "Rapiers: " + str(rapiers) + "\n"
        response += "Staves: " + str(staves) + "\n"
        response += "Faceguards: " + str(faceguards) + "\n"
        response += "Chestguards: " + str(chestguards) + "\n"
        response += "Legguards: " + str(legguards) + "\n"
        response += "Scythes: " + str(scythes) + "\n"

    else:
        diceroll = random.uniform(0, 173)
        if diceroll <= 1:
            response = "Scythe of Vitur (" + str(diceroll) + ")"
        elif diceroll <= 10:
            decent_loot = [
                'Ghazri Rapier',
                'Sanguinesti Staff',
                'Justiciar Faceguard',
                'Justiciar Chestguard',
                'Justiciar Legguards'
            ]
            response = random.choice(decent_loot) + " (" + str(diceroll) + ")"
        elif diceroll <= 21:
            response = "Avernic defender hilt (" + str(diceroll) + ")"
        else:
            response = "Cabbage get fukt (" + str(diceroll) + ")"
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