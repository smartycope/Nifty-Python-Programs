import tkinter as tk
from tkinter import filedialog
import os
from os import path as p
 
justJSON = False
nameCount = 0
items = {}
 
# name = input('The name of this recipe is: ')
# namespace = name
# shaped = input('Is this recipe shaped? (y/n) (only shaped recipies are currently supported): ').lower() == 'y'
shaped = True
pattern = [input('Enter the recipe:\n'), input(''), input('')]
 
 
def getUniqueName():
    global nameCount
    nameCount += 1
    return str(nameCount)
 
def printList(l):
    return str(l).replace("'", '"')
 
 
def getBlock(input):
    input = input.replace(" ", "")
    if input.startswith('minecraft:'):
        return input
    else:
        return 'minecraft:' + input
 
def getBlocks(input):
    input = input.replace(" ", "")
    if ',' in input:
        return [getBlock(i) for i in input.split(',')]
    else:
        return getBlock(input)
 
 
for line in pattern:
    for char in line:
        if char != ' ' and char not in items.keys():
            items[char] = getBlocks(input(f'{char} stands for (enter the id tag): '))
 
 
result = getBlock(input('This recipe gives you (enter the id tag): '))
name = namespace = result[10:]
resultAmount = input('How many? ')
 
# Get The save we're adding this to
root=tk.Tk()
# try:
savePath = filedialog.askdirectory(initialdir=os.path.expanduser("~/AppData/Roaming/.minecraft/saves/"), title='Pick Save', mustexist=True)
# except:
#     savePath = None
 
# print('~', savePath, '~', type(savePath))
 
# if savePath is not str:
#     savePath = input('Please manully input a path then: ')
 
# print('-', savePath, '-')
 
# if not p.isdir(savePath):
#     print('Sorry, that\'s not a valid folder path.')
#     exit()
 
root.destroy()
 
 
# savePath = '/home/marvin/hello/tmp/fakeSave'
 
 
tags = {}
 
for key, val in items.items():
    if type(val) is list:
        tags[key] = getUniqueName()
 
# Make the folders
if not justJSON:
    path = p.join(p.join(savePath, 'datapacks'), name)
    if not os.path.exists(path):
        os.mkdir(path)
 
    dataPath = p.join(path, 'data')
    if not os.path.exists(dataPath):
        os.mkdir(dataPath)
 
    namespacePath = p.join(dataPath, namespace)
    if not os.path.exists(namespacePath):
        os.mkdir(namespacePath)
 
    minecraftPath = p.join(dataPath, 'minecraft')
    if not os.path.exists(minecraftPath):
        os.mkdir(minecraftPath)
 
    recipesPath = p.join(minecraftPath, 'recipes')
    if not os.path.exists(recipesPath):
        os.mkdir(recipesPath)
 
    tagPath = p.join(namespacePath, 'tags')
    if not os.path.exists(tagPath):
        os.mkdir(tagPath)
 
    itemsPath = p.join(tagPath, 'items')
    if not os.path.exists(itemsPath):
        os.mkdir(itemsPath)
 
    # Now make the files
    with open(p.join(path, "pack.mcmeta"), 'w') as f:
        f.write(f'''{{\n        "pack": {{\n            "pack_format": 5,\n            "description": "An auto generated datapack to hold the {name} recipe. Made by Copeland Carter"\n        }}\n    }}''')
 
    for key, _name in tags.items():
        with open(p.join(itemsPath, _name + '.json'), 'w') as f:
            f.write(f'''{{\n    "replace": false,\n     "values": {printList(items[key])}\n}}''')
 
 
with open(p.join(savePath if justJSON else recipesPath, name + '.json'), 'w') as f:
    f.write(f'''{{\n    "type": "{"crafting_shaped" if shaped else "crafting_shaped"}",\n    "pattern": {printList(pattern)},\n    "key": {{\n''')
 
    i=0
    for key, item in items.items():
        i+=1
        f.write(f'        "{key}": {{\n            "{"tag" if type(item) is list else "item"}": "{name + ":" + tags[key] if type(item) is list else item}"\n        }}')
        if i != len(items):
            f.write(',\n')
 
    f.write(f'''\n    }},\n    "result": {{\n        "item": "{result}",\n        "count": {resultAmount}\n    }}\n}}''')
 
 
print("\nSuccess!")
