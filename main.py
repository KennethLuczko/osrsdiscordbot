import os
import random
import json
from collections import Counter
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

def subList(itemString, listObject, subLists):
#Recursive function, takes an item (itemString), a list object from the initial json(listObject)...
#...aswell as the imported jsons(subLists)
    returnArray = []
    diceArray = []
    weight = 0
    for object in itemString:
        for item in subLists:
            if object in item.keys(): #Found a match for our item in the imported json lists...
               # print(f'GWRareTable Check: {object}')   #...our item is confirmed to be a sub list
                for i in range(0, len(item[object])):
                    if "item" in item[object][i]:
                        for j in range(0, item[object][i]["weight"]):
                            diceArray.append(item[object][i]["item"])     #Create a weight array
                        weight += item[object][i]["weight"]
                        
                    elif "bonus" in item[object][i]:
                        if random.randint(1, item[object][i]["chance"]) == 1: #hit the 1 in however many
                            returnArray.append(item[object][i]["bonus"])
                    else: #GUARANTEED
                        returnArray.append(item[object][i]["guaranteed"])
                diceroll = random.randint(0, weight-1)#Create a weight value for dice roll
                returnArray.append(diceArray[diceroll])

                 
    
        if object in listObject.keys():      #Found a match for our item in the original json...    
            #print(f'bandosLoot Check: {object}')
            
            weight = 0                       #... our item is confirmed to be a sub list
            returnArray = []
            diceArray = []
            for i in range(0, len(listObject[object])):
                if "item" in listObject[object][i]:    
                    for j in range(0, listObject[object][i]["weight"]):
                        diceArray.append(listObject[object][i]["item"])   #Create a weight array
                    weight += listObject[object][i]["weight"]               #Create a weight value for dice roll
                elif "bonus" in listObject[object][i]:
                    bonusDice = random.randint(1, listObject[object][i]["chance"])  
                    if bonusDice == 1:
                        returnArray.append(listObject[object][i]["bonus"])
                else: #GUARANTEED
                    returnArray.append(listObject[object][i]["guaranteed"])

            diceroll = random.randint(0, weight-1)                          #Roll the dice...
            returnArray.append(diceArray[diceroll])
                                                                            #...and recursively check if our dice roll...
                                                                            #...landed on yet another sublist. If not, return item.
        else:
            print(f'Not a sublist: {object}')
            return itemString       #Our item is not a sub list, return the item.

    return subList(returnArray, listObject, subLists)

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
        for i in range(0, int(arg)):
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
    
# ------ GENERAL GRAARDOR (BANDOS)
@bot.command(name='Bandos', help='Returns the loot from General Graardor.')
async def Bandos(Bandos, *args):
    f = open('bandosLoot.json')
    g = open('GWRareTable.json')
    jsonsubLists = [json.load(g)]
    jsondata = json.load(f)
    weight = 0 #initial weight value of 0, add weight values from the json
    array = [] #initial empty array, fill the array with the items, one array slot per weight
    for i in range (0, len(jsondata["bandosLoot"]["pool"])):
        if "item" in jsondata["bandosLoot"]["pool"][i]:
            for j in range(0, jsondata["bandosLoot"]["pool"][i]["weight"]):
                array.append(jsondata["bandosLoot"]["pool"][i]["item"]) #Create array with each item added once per weighting
            weight += jsondata["bandosLoot"]["pool"][i]["weight"]       #Add weights together for a diceroll
        
    if not args:
        response = ""
        responselist = []
        ###WEIGHTED ITEMS###
        responselist.append(subList([array[random.randint(0, weight-1)]], jsondata["bandosLoot"], jsonsubLists)) #Single Dice Roll
        ###GUARANTEED ITEMS###
        for item in jsondata["bandosLoot"]["pool"]:       #Add guaranteed loot
            if "guaranteed" in item:
                responselist.append(subList([item["guaranteed"]], jsondata["bandosLoot"], jsonsubLists))
        ###BONUS ITEMS###
        for i in range(0, len(jsondata["bandosLoot"]["pool"])):
            if "bonus" in jsondata["bandosLoot"]["pool"][i]:
                if random.randint(1, jsondata["bandosLoot"]["pool"][i]["chance"]) == 1: #hit the 1 in however many
                    array.append(jsondata["bandosLoot"]["pool"][i]["bonus"])
        
        for item, value in Counter(responselist).items():       #Add the tally...
            response += item + " x" + (str(value)) + "\n"       #...and format the output a bit

    elif args[0].isnumeric():
        response = ""
        responselist = []
        for i in range(0, int(args[0])):
            ###WEIGHTED ITEMS###
            diceroll = random.randint(0, weight-1)                  #Multiple Dice Rolls
            responselist.append(subList([array[diceroll]], jsondata["bandosLoot"], jsonsubLists))
            ###GUARANTEED ITEMS###
            for item in jsondata["bandosLoot"]["pool"]:       #Add guaranteed loot
                if "guaranteed" in item:
                  responselist.append(subList([item["guaranteed"]], jsondata["bandosLoot"], jsonsubLists))
            ###BONUS ITEMS###
            for i in range(0, len(jsondata["bandosLoot"]["pool"])):
                if "bonus" in jsondata["bandosLoot"]["pool"][i]:
                    bonusDice = random.randint(1, jsondata["bandosLoot"]["pool"][i]["chance"])
                    if bonusDice == 1: #hit the 1 in however many
                        print("YATZEE")
                        responselist.append([jsondata["bandosLoot"]["pool"][i]["bonus"]])
                        print(jsondata["bandosLoot"]["pool"][i]["bonus"])
            print(f'Diceroll: {diceroll} - Item: {array[diceroll]}')
        #print(responselist)
        responseFinal = []
        for item in responselist:
            for object in item:
                responseFinal.append(object)                                                  #Add the tally...
        for item in Counter(responseFinal):
            response += item + " x" + (str(Counter(responseFinal)[item])) + "\n"           #...and format the output a bit
        
    else:
        response = "Argument is not a number"



    await Bandos.send(response)
bot.run(TOKEN)