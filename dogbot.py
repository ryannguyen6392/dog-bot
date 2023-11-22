import os
import time
import random as Rand
import json
import discord
from munch import munchify
import math
from threading import Timer  
from google_images_search import GoogleImagesSearch
from io import BytesIO
from PIL import Image
import requests

class Dog:
    def __init__(self, id):
        self.id = id
        self.name = ""
        self.hnum = 5
        self.hunger = 5
        self.dist = 0.0
        self.cooking = False
        self.food = None
        self.walking = False
        self.almost_leaving = False
        self.size = ""
        self.color = ""
        self.breed = ""    
        self.almost_chosen = False      
        self.pictures = []
        self.coins = 0

def hasDog(dogs, id):
    for dog in dogs:
        if id == dog.id:
            return True
    return False

def findDog(dogs, id):
    for dog in dogs:
        if id == dog.id:
            return dog
    return False

async def showDog(user, dogs):
    dog = findDog(dogs, user.id)
    picture = Image.open(BytesIO(requests.get(dog.pictures[0]).content))
    my_bytes_io = BytesIO()
    my_bytes_io.seek(0)
    picture.save(my_bytes_io, picture.format)
    my_bytes_io.seek(0)
    fi = discord.File(my_bytes_io, filename="image.png")
    await user.send(file=fi)
    my_bytes_io.close()

    name = dog.name
    dist = dog.dist
    hunger = ""
    coins = dog.coins
    coin_emoji = "\U0001F4B0"
    for h in range(dog.hunger):
        hunger += "\U0001F357"
    await user.send(f"``` {name} \n-------------------------------------\n\tHappiness: MEGA HAPWY\n\tHunger: {hunger}\n\tDistance Walked: {dist} mi\n\tMoneys: {coins} {coin_emoji}```")

def save_dogs(pets, dogs):
    with open('pets.txt', 'w') as outfile:
        save_pets = pets
        dogs_flatten = []
        for dog in dogs:
            dogs_flatten.append(vars(dog))
        save_pets['dogs'] = dogs_flatten
        json.dump(save_pets, outfile)

async def sub(message, subs):
    if message.author.dm_channel == None:
        await message.author.create_dm()
    if  message.author.id not in subs['dm_ids']:
        subs['dm_ids'].append(message.author.id)
        with open('subs.txt', 'w') as outfile:
            json.dump(subs, outfile)
        await message.author.send("welcome to dog bot\n\n")
        dogs.append(Dog(message.author.id))
        save_dogs(pets, dogs)
        await message.author.send("what dog breed are u looking for?\n\n")

async def choose_dog(message, dog):
    google.search({'q': f"{dog.size} {dog.color} {dog.breed}", 'num': 10,'fileType': 'jpg|gif|png', 'imgType': 'photo', 'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'})
    results = google.results()
    print(results)
    i = 1
    for image in results:
        dog.pictures.append(image.url)
        my_bytes_io = BytesIO()
            # here we tell the BytesIO object to go back to address 0
        my_bytes_io.seek(0)

            # or without the raw data which will be automatically taken
            # inside the copy_to() method
        image.copy_to(my_bytes_io)

            # we go back to address 0 again so PIL can read it from start to finish
        my_bytes_io.seek(0)
            
        fi = discord.File(my_bytes_io, filename="image.png")
        await message.channel.send(f"{i}.")
        await message.channel.send(file=fi)
        my_bytes_io.close()
        i +=1
    await message.channel.send("choose a number!")

async def walk_dog(message, pets, dogs):
    dog = findDog(dogs, message.author.id)
    walk_string = "walk"
    w = await message.channel.send(f"```{walk_string}```")
    time.sleep(1)
    for i in range(4):
        walk_string += " walk"
        if Rand.random() > 0.5:
            walk_string += "ing"
        await w.edit(content=f"```{walk_string}```")
        time.sleep(1)
    dog.hunger -= 1
    dog.dist += 1
    save_dogs(pets, dogs)
    await w.edit(content="done walking")

async def rename_dog(message, pets, dogs):
    dog = findDog(dogs, message.author.id)
    dog.name = message.content.replace("rename ", "")
    await message.author.send("dog renamed")
    save_dogs(pets, dogs)

def hunger(pets, dogs):
    for dog in dogs:
        if(dog.hunger > 0):
            dog.hunger -= 1
    save_dogs(pets, dogs)

class RepeatTimer(Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  

PROTEIN = "beef pork chicken"
VEGETABLES = "carrots onions peas zucchini spinach"
GRAINS = "white rice brown rice quinoa"

client = discord.Client(intents=discord.Intents(messages=True))
with open('subs.txt') as json_file:
    subs = json.load(json_file)
with open('pets.txt') as json_file:
   pets = json.load(json_file)
dogs = []
for dog in pets['dogs']:
    dogs.append(munchify(dog))

global_hunger = RepeatTimer(3600, hunger, [pets, dogs])
global_hunger.daemon = True

google = GoogleImagesSearch('AIzaSyCMv6369X227JMBN6Traw3H9-PXQNKzkOA', 'd79290980bda647e7')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global_hunger.start()
            
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    if message.content == "doge me":
        await message.channel.send("ur subscribed")
        await sub(message, subs)
    elif isinstance(message.channel, discord.DMChannel) and message.author.id in subs['dm_ids']:
        dog = findDog(dogs, message.author.id)
        if not dog.breed:
            dog.breed = message.content
            await message.channel.send("what size are u looking for?")
        elif not dog.size:
            dog.size = message.content
            await message.channel.send("what color are u looking for?")
        elif not dog.color:
            dog.color = message.content
            await message.channel.send(f"sounds like you want a {dog.size}, {dog.color} {dog.breed}, is that correct?")
            dog.almost_chosen = True
            return
        if message.content == "yes" and dog.almost_chosen:
            await choose_dog(message, dog)
            dog.almost_chosen = False
            return
        elif message.content == "no" and dog.almost_chosen:
            dog.almost_chosen = False
            dog.breed = ""
            dog.size = ""
            dog.color = ""
            await message.channel.send("let's try this again\nwhat dog breed are you looking for?")
            return

        if len(dog.pictures) > 1:
            dog.pictures = [dog.pictures[int(message.content) - 1]]
            await message.channel.send("cute! what're you gonna name them?")
            return
    
        if dog.breed and dog.color and dog.size and dog.name == "":
            dog.name = message.content
            save_dogs(pets, dogs)
            await message.channel.send(f"nice! i hope {dog.name} likes u! (try using \"my\" to see their stats)")

        if message.content == "my":
            await showDog(message.author, dogs)
        if message.content == "walk" and not dog.walking:
            if dog.hunger > 1:
                dog.walking = True
                await walk_dog(message, pets, dogs)
                dog.walking = False
            else:
                await message.channel.send(f"{dog.name} is too hungry!")
        if message.content.startswith("rename"):
            await rename_dog(message, pets, dogs)
        if message.content == "cook":
            dog.cooking = True
            await message.channel.send(f"cooking Time!\n```{PROTEIN}```choose a protein!")
            dog.food = {}
        if dog.cooking and (message.content.lower() in PROTEIN or message.content.lower() in VEGETABLES or message.content.lower() in GRAINS):
            if message.content.lower() in PROTEIN:
                dog.food['protein'] = message.content.lower()
                await message.channel.send(f"```{VEGETABLES}```now choose some vegetables!")
            elif message.content.lower() in VEGETABLES:
                dog.food['vegetables'] = message.content.lower()
                await message.channel.send(f"```{GRAINS}```finish with some grains!")
            elif message.content.lower() in GRAINS:
                dog.food['grain'] = message.content.lower()
                await message.channel.send(f"nice cooking!\nHeres what you made:\n```yum yum tums\n\tprotein - {dog.food['protein']}\n\tvegetables - {dog.food['vegetables']}\n\tgrain - {dog.food['grain']}```")
                dog.cooking = False
            else:
                await message.channel.send("that's not an ingredient!")
        if message.content == "feed":
            if dog.food is not None:
                await message.channel.send(f"```{dog.name}: bork!```")
                await message.channel.send("i think that means yum....?")
                dog.hunger += 3
                dog.food = None
                save_dogs(pets, dogs)
            else:
                await message.channel.send("you have no food!")
        if "pet" in message.content.lower() or "pat pat" in message.content.lower():
            await message.author.send("_**PETTING INTESIFIES**_")
            fi = discord.File(fp='C:/Users/ryann/OneDrive/Desktop/discord bot/doge eyes.jpg', filename='doge eyes.jpg')
            await message.author.send(file=fi)
        if message.content == "leave":
            await message.channel.send(f"you're really leaving __{dog.name}__?")
            await message.channel.send("---------\nyes | **NO**\n---------")
            dog.almost_leaving = True
        if dog.almost_leaving:
            if message.content == "yes":
                dogs.remove(dog)
                save_dogs(pets,dogs)
                await message.channel.send(f"**YOU MONSTER**")
                subs['dm_ids'].remove(message.author.dm_channel.id)
                with open('subs.txt', 'w') as outfile:
                    json.dump(subs, outfile)
                await message.channel.send(f"unsubbed")
            elif message.content == "no":
                dog.almost_leaving = False
                await message.channel.send("nice choice")
        

client.run("ODk5MDAyMDk0MDE3NzI4NTMz.GjhlvC.ZbyuODUT77vl86VJbJ99FxtdufQLGDq4VHaJKM")