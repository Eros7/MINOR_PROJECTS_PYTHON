import discord
import os
import requests
import json
import random

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

  if any(word in msg for word in sadwords):
    await message.channel.send(random.choice(starter_encouragements))

client.run(os.environ['TOKEN'])

