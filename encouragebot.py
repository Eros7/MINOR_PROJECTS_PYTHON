import discord
import os
import requests
import json
import random
from replit import db

intents=discord.Intents.default()
intents.message_content=True
client=discord.Client(intents=intents)

sadwords=['depressed','sad','unhappy','angry','tired','wary']

starter_encouragements=['Cheer up','Hang in there',"You're a great person"]

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+' - '+json_data[0]['a']
  return(quote)


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
    print(db["encouragements"])
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
  encouragements=[]
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event  
async def on_message(message):
  if message.author==client.user:
    return
  msg=message.content
  if msg.startswith('$hello'):
    await message.channel.send('Hello! {0.author}'.format(message))
  

  if msg.startswith('$inspire'):
    await message.channel.send(get_quote())

  options=starter_encouragements
  if "encouragements" in db.keys():
    options = options.extend(db["encouragements"])
  
  if any(word in msg for word in sadwords):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message=msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if msg.startswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements=db["encouragements"]
      await message.channel.send(encouragements)
  
client.run(os.environ['TOKEN'])

