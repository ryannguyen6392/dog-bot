import os
import time
import random
import json
import discord
from munch import munchify
from PIL import Image
from io import BytesIO
from sympy import Point, Line, pi
import math
import random

class Dog:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.hnum = 5
        self.hunger = 5
        self.dist = 0.0
        self.fetching = False
        self.fetch_dist = -1
        self.fetch_ang = -1
        self.cooking = False
        self.food = None
        self.walking = False

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
    await user.send("ur dog is")
    dog = findDog(dogs, user.dm_channel.id)
    name = dog.name
    dist = dog.dist
    hunger = ""
    for h in range(dog.hunger):
        hunger += "\U0001F357"
    await user.send(f"``` {name} \n-------------------------------------\n\tHappiness: MEGA HAPWY\n\tHunger: {hunger}\n\tDistance Walked: {dist} mi```")

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
    if  message.author.dm_channel.id not in subs['dm_ids']:
        subs['dm_ids'].append(message.author.dm_channel.id)
        with open('subs.txt', 'w') as outfile:
            json.dump(subs, outfile)
        await message.author.send("welcome to dog bot\n\n")
        await message.author.send("enter the name of ur doge")

async def new_dog(message, pets, dogs):
    dogs.append(Dog(message.author.dm_channel.id, message.content))
    await showDog(message.author, dogs)
    save_dogs(pets, dogs)

async def walk_dog(message, pets, dogs):
    dog = findDog(dogs, message.author.dm_channel.id)
    walk_string = "walk"
    w = await message.channel.send(f"```{walk_string}```")
    time.sleep(1)
    for i in range(4):
        walk_string += " walk"
        if random() > 0.5:
            walk_string += "ing"
        await w.edit(content=f"```{walk_string}```")
        time.sleep(1)
    dog.hunger -= 1
    dog.dist += 1
    save_dogs(pets, dogs)
    await w.edit(content="done walking")

async def rename_dog(message, pets, dogs):
    dog = findDog(dogs, message.author.dm_channel.id)
    dog.name = message.content.replace("rename ", "")
    await message.author.send("dog renamed")
    save_dogs(pets, dogs)

PROTEIN = "beef pork chicken"
VEGETABLES = "carrots onions peas zucchini spinach"
GRAINS = "white rice brown rice quinoa"

client = discord.Client()

with open('subs.txt') as json_file:
    subs = json.load(json_file)
with open('pets.txt') as json_file:
   pets = json.load(json_file)
dogs = []
for dog in pets['dogs']:
    dogs.append(munchify(dog))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #mem = await client.guilds[0].query_members("Ryan")
    #await send_dm(mem[0], "pet me!")
            
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "doge me":
        await message.channel.send("ur subscribed")
        await sub(message, subs)
    if isinstance(message.channel, discord.DMChannel) and message.author.dm_channel is not None and message.author.dm_channel.id in subs['dm_ids']:
        if not [dog for dog in dogs if dog.id == message.author.dm_channel.id]:
            await new_dog(message, pets, dogs)
        else:
            dog = findDog(dogs, message.author.dm_channel.id)
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
            if message.content == "feed" and dog.food is not None:
                await message.channel.send(f"```{dog.name}: bork!```")
                await message.channel.send("i think that means yum....?")
                dog.hunger += 3
                dog.food = None
                save_dogs(pets, dogs)
            elif message.content == "feed":
                await message.channel.send("you have no food!")
            if message.content == "fetch":
                dog.fetching = True
                avatar = Image.open(BytesIO(await message.author.avatar_url.read()))
                background = Image.open('C:/Users/ryann/OneDrive/Desktop/discord bot/background.png')
                dog_image = Image.open('C:/Users/ryann/OneDrive/Desktop/discord bot/shiba crop.jpg')

                background = background.resize((700, 700)).convert('RGBA')
                avatar = avatar.resize((75, 75)).convert('RGBA')
                dog_image = dog_image.resize((75, 75)).convert('RGBA')

                dog_pos = (random.randint(0,background.width - dog_image.width), random.randint(0,int(background.height/3 - dog_image.height)))
                avatar_pos = (random.randint(0,background.width - avatar.width), random.randint(int(2 * background.height/3),background.height - avatar.height))
                dog_center = Point(dog_pos[0] + dog_image.width/2, dog_pos[1] + dog_image.height/2)
                avatar_center = Point(avatar_pos[0] + avatar.width/2, avatar_pos[1] + avatar.height/2)

                dog.fetch_avatar_pos = avatar_center

                l1 = Line(avatar_center, dog_center)
                l2 = Line((0,0), (-1, 0))
                dog.fetch_dist = int(dog_center.distance(avatar_center))
                dog.fetch_ang = int(math.degrees(l1.angle_between(l2)))

                print("Fetch Command Registered")
                print(f"Name: {message.author.name} | Dog: {dog.name}")
                print(f"Angle: {dog.fetch_ang}")
                print(f"Power: {dog.fetch_dist/50} | Distance: {dog.fetch_dist}")
                
                background.paste(dog_image, dog_pos, dog_image)
                background.paste(avatar, avatar_pos, avatar)
                dog.fetch_img = background

                my_bytes_io = BytesIO()
                my_bytes_io.seek(0)
                background.save(my_bytes_io, format='png')
                my_bytes_io.seek(0)

                fi = discord.File(my_bytes_io, filename="image.png")
                await message.channel.send(file=fi)
                my_bytes_io.close()

                await message.channel.send("Instructions: Try to get the ball as close as you can!\nInput:(_Angle_, _Power_)")
            if dog.fetching and message.content.startswith('('):
                input = message.content.replace('(', '').replace(')', '').split(', ')
                if len(input) == 2 and input[0].isnumeric() and input[1].isnumeric():

                    throw = float(input[1]) * 50
                    if dog.fetch_ang - 5 <= int(input[0]) <= dog.fetch_ang + 5 and dog.fetch_dist - 20 <= throw <= dog.fetch_dist + 20:
                        await message.channel.send("You did it!")
                        dog.fetching = False
                    else:
                        dot = Image.open('C:/Users/ryann/OneDrive/Desktop/discord bot/red dot.jpg')
                        dot = dot.resize((20, 20)).convert('RGBA')
                        dot_pos = (dog.fetch_avatar_pos[0] - dot.width/2 - int(throw * math.cos(math.radians(int(input[0])))), dog.fetch_avatar_pos[1] - dot.height/2 - int(throw * math.sin(math.radians(int(input[0])))))
                        dog.fetch_img.paste(dot, dot_pos, dot)
                        my_bytes_io = BytesIO()
                        my_bytes_io.seek(0)
                        dog.fetch_img.save(my_bytes_io, format='png')
                        my_bytes_io.seek(0)

                        fi = discord.File(my_bytes_io, filename="image.png")
                        await message.channel.send(file=fi)
                        my_bytes_io.close()
                        await message.channel.send("Try again!")
                else:
                    await message.channel.send("Invalid Input")
            

        if "pet" in message.content.lower() or "pat pat" in message.content.lower():
            await message.author.send("_**PETTING INTESIFIES**_")
            fi = discord.File(fp='C:/Users/ryann/OneDrive/Desktop/discord bot/doge eyes.jpg', filename='doge eyes.jpg')
            await message.author.send(file=fi)


async def send_dm(mem, string):
    if mem.dm_channel == None:
        await mem.create_dm()
    await mem.dm_channel.send(string)

client.run("ODk5MDAyMDk0MDE3NzI4NTMz.YWsa8Q.b-WWe5VM2jQeO8weZTksH_IEfVs")