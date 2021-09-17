import discord
import os
import requests
import json

client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '" -' + json_data[0]['a']
  return(quote)

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

  if msg.content.startswith('$motivasi'):
    quote = get_quote()
    await msg.channel.send(quote)
  
client.run(os.getenv("DISCORD_BOT_TOKEN"))