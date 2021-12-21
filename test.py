import os
import json
import random

from collections import Counter




def lootTable(table, tables):
    weightPool = 0
    weightArray = []
    finalLootArray = []
    for item in table:
        if "item" in item:
            for i in range(0, item["weight"]):
                weightArray.append(item["item"])
            weightPool += item["weight"]
        elif "guaranteed" in item:
            finalLootArray.append(subTable(item["guaranteed"], tables))
        elif "bonus" in item:
            bonusDice = random.randint(0, item["chance"])
            if bonusDice == 1:
                finalLootArray.append(subTable(item["bonus"], tables))
    weightDice = random.randint(0, weightPool-1)
    print(weightArray[weightDice])
    finalLootArray.append(subTable(weightArray[weightDice], tables))
    return finalLootArray


def subTable(item, tables):
    for table in tables:
        for key in table.keys():
            if item == key:             #Our item is a table
                print("Found Table")
                print(table[item])
                return lootTable(table[item], tables)
    return item


def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])



f = open('bandosLoot.json')
g = open('GWRareTable.json')

jsontables = [json.load(f), json.load(g)]

response = ""
resultlist = subTable("generalTable", jsontables)
for item in Counter(flatten(resultlist)):
    response += item + " x" + str(Counter(flatten(resultlist))[item]) + "\n"
print(response)
