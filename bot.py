import os
import time
import random
import discord
from google_images_search import GoogleImagesSearch
from io import BytesIO
import requests
from PIL import Image, ImageEnhance

client = discord.Client()
google = GoogleImagesSearch('AIzaSyCMv6369X227JMBN6Traw3H9-PXQNKzkOA', 'c467ed045c57f4cd1')
queue = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #mem = await client.guilds[0].query_members("")
    #await send_dm(mem[0], "u smell!")

    #messages = await client.guilds[0].get_channel(702671662130397208).history(limit=20).flatten()
    #for msg in messages:
    #    if "INTERNSHIP" in msg.content:
    #        while True:
    #            await msg.add_reaction(await msg.guild.fetch_emoji(704213530307592244))
    #            time.sleep(1)
    #            await msg.clear_reactions()
            

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.display_name == "dean hu tran":
      await message.channel.send("shut up kevin")
    if "nigga" in message.content.lower():
        for num in range(1):
            await message.channel.send("AY")
            time.sleep(0.1)
    if message.content.startswith("search"):
        google.search({'q': message.content.replace("search ", ''), 'num': 10,'fileType': 'jpg|gif|png'})
        results = google.results()
        print(results)
        image = random.choice(results)
        my_bytes_io = BytesIO()
            # here we tell the BytesIO object to go back to address 0
        my_bytes_io.seek(0)

            # or without the raw data which will be automatically taken
            # inside the copy_to() method
        image.copy_to(my_bytes_io)

            # we go back to address 0 again so PIL can read it from start to finish
        my_bytes_io.seek(0)
            
        fi = discord.File(my_bytes_io, filename="image.png")
        await message.channel.send(file=fi)
        my_bytes_io.close()
        #for img in google.results():
        #    google.results().pop()

    if message.content.startswith("!deepfry"):
        queue.append(message.author)
    if queue and message.attachments and message.author in queue:
        response = requests.get(message.attachments[0].url)
        img = Image.open(BytesIO(response.content))

        new_img = deepfry(img)

        my_bytes_io = BytesIO()
        my_bytes_io.seek(0)
        new_img.save(my_bytes_io, img.format)
        my_bytes_io.seek(0)

        fi = discord.File(my_bytes_io, filename="image.png")
        await message.channel.send(file=fi)
        my_bytes_io.close()
        queue.remove(message.author)
    


def deepfry(img):
    i1 = ImageEnhance.Brightness(img)
    i2 = i1.enhance(5)
    i3 = ImageEnhance.Color(i2)
    i4 = i3.enhance(5)
    i5 = ImageEnhance.Contrast(i4)
    i6 = i5.enhance(5)
    i7 = ImageEnhance.Sharpness(i6)
    i8 = i7.enhance(5)
    return i8

async def send_dm(mem, string):
    if mem.dm_channel == None:
        await mem.create_dm()
    await mem.dm_channel.send(string)

@client.event
async def on_reaction_add(reaction, user):
    print("whoops")

client.run("ODk4NDA0MTEzNDIxODQwNDE1.YWjuCA.bFtPmTx3orSc-RgXBmNbTjBc5Go")