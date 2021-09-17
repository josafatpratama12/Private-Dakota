import discord
import os

client = discord.Client()

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):
  if msg.author == client.user:
    return
  
  if msg.content.startswith('$halo'):
    await msg.channel.send('Nyahalo!')
  
  if msg.content.startswith('$bilang'):
    msg_content = msg.content
    await msg.channel.send(msg.content.replace("$bilang",""))
  
client.run(os.getenv("DISCORD_BOT_TOKEN"))