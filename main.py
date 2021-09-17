import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

lamaran = ["dakota mau ga jadi pacarku", "dakota mau ga jadi pacarku?", "dakota mau jadi pacarku ga?", "dakota mau ndak jadi pacarku?", "dakota mau ngga jadi pacarku", "dakota mau jadi pacarku ga", "dakota mau a jadi pacarku"]

sad_words = ["hadeh", "capek", "mboh", "mboh wes cok mumet aku","nangis"]

starter_encouragements = [
  "Sini aku pelukk~",
  "Cheer Up! :3",
  "Jangan sedih, dakota sayang kamu ^^"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = '"' + json_data[0]['q'] + '" -' + json_data[0]['a']
  return(quote)

def update_encouragement(enc_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(enc_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enc_msg]
  
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

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
    await msg.channel.send(msg_content.replace("$bilang",""))

  if any(word in msg.content.lower() for word in lamaran ):
    if(msg.author.name == "Ichika"):
      await msg.channel.send("Mauuuuu")
    else:
      await msg.channel.send("Maaf, aku udah sayang yosaa~")

  if msg.content.startswith('$motivasi'):
    quote = get_quote()
    await msg.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in msg.content for word in sad_words):
      await msg.channel.send(random.choice(options))
  
  if msg.content.startswith("$perhatian"):
    value = msg.content.split("$perhatian ",1)[1]

    if value.lower() == "iya":
      if db["responding"]:
        await msg.channel.send("Dakota sudah perhatian ke kalian kok~")
      else:
        db["responding"] = True
        await msg.channel.send("Dakota akan kasih perhatian lebih untuk kalian~")

    elif value.lower() == "tidak":
      db["responding"] = False
      await msg.channel.send("Baiklah, dakota akan memberi kalian waktu sendiri, tetap semangat ya~")
    
    else:
      await msg.channel.send("Maaf, dakota hanya tau iya atau tidak untuk perintah itu ehee~")

  if msg.content.startswith('$semangat'):
    encouraging_msg = msg.content.split("$semangat ",1)[1]
    update_encouragement(encouraging_msg)
    await msg.channel.send("Baik, dakota sudah mempelajari kalimat semangat itu~")
  
  if msg.content.startswith('$cek'):
    encouragements = db["encouragements"]
    all_enc_msg = "Kata penyemangat yang dakota sudah pelajari:"
    for enc_msg in encouragements.value:
      all_enc_msg = all_enc_msg + "\n" + enc_msg
    await msg.channel.send(all_enc_msg)

  if msg.content.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.content.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await msg.channel.send(encouragements.value)

keep_alive()
client.run(os.getenv("DISCORD_BOT_TOKEN"))