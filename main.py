import os
import random
import json
import sys

sys.setrecursionlimit(10000) #THIS IS NOT SMART PROBABLY
from collections import Counter
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


#Function to roll out a table when called
def lootTable(table, tables): 
    weightPool = 0
    weightArray = []
    finalLootArray = []
    for item in table:
        ##WEIGHTED ITEMS###
        if "item" in item:
            for i in range(0, item["weight"]):
                weightArray.append(item["item"])
            weightPool += item["weight"]
        ###GUARANTEED ITEMS###
        elif "guaranteed" in item:
            finalLootArray.append(subTable(item["guaranteed"], tables))
        ###BONUS/TERTIARY ITEMS###
        elif "bonus" in item:
            bonusDice = random.randint(0, item["chance"])
            if bonusDice == 1:
                finalLootArray.append(subTable(item["bonus"], tables))
    weightDice = random.randint(0, weightPool-1)
    finalLootArray.append(subTable(weightArray[weightDice], tables))
    return finalLootArray

#Function to detect if the rolled out item is a subtable or an item
def subTable(item, tables):
    for table in tables:
        for key in table.keys():
            if item == key:             #Our item is a table
                return lootTable(table[item], tables)
    return item #Item is not a table, return it


def flatten(S): #Function to flatten lists within lists, super inefficient recursive bad lolz
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])



@bot.command(name='Bandos', help='Returns the loot from General Graardor.')
async def Bandos(Bandos, *args):
    print("Bandos command called")
    f = open('bandosLoot.json')
    g = open('GWRareTable.json')

    jsontables = [json.load(f), json.load(g)]
    if not args:
        response = ""
        resultlist = subTable("generalTable", jsontables)
        for item in Counter(flatten(resultlist)):
            response += item + " x" + str(Counter(flatten(resultlist))[item]) + "\n"

    elif args[0].isnumeric():
        print("Iterations: " + args[0])
        response = ""
        resultlist = []
        for i in range(0, int(args[0])):
            resultlist.append(subTable("generalTable", jsontables))
        flattenresult = flatten(resultlist)
        countedResult = Counter(flattenresult)
        for item in countedResult:
            response += item + " x" + str(countedResult[item]) + "\n"
    else:
        response = "Argument is not a number"

    await Bandos.send(response)
bot.run(TOKEN)