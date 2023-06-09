import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive



intents=discord.Intents.default()
intents.message_content=True
client=discord.Client(intents=intents)

sadwords=['depressed','sad','unhappy','angry','tired','wary']

starter_encouragements=['Cheer up','Hang in there',"You're a great person"]

if "responding" not in db.keys():
  db["responding"]=True
  

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

  if db["responding"]:
    options=starter_encouragements
    if "encouragements" in db.keys():
      options = options+list(db["encouragements"])
    
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

  if msg.startswith("$list"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value=msg.split("$responding ",1)[1]
    if value.lower() =="true":
      db["responding"]=True
      await message.channel.send("Responding in ON")
    else:
      db["responding"]=False
      await message.channel.send("Responding in OFF")
      
keep_alive()
client.run(os.environ['TOKEN'])

#BOT HOSTED THROUGH REPLIT