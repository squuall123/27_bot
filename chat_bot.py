import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

# Init
db["responding"] = True

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!",
  "I'm here for you!"
]

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
hachwa_words = ["tle3t", "nikthom", "nikt", "7chitou"]

# get random inspiring quote from the net
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# Update new encouragement to 27 bot
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

# Delete encouragement from 27 bot
def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

# Callback when bot is ready
@client.event
async def on_ready():
    
    print('We have logged in as {0.user}'.format(client))
    print(client.user.name)
    print(client.user.id)
    print('------')

    #if server:
    #    for member in server.members:
    #        print('name: {}'.format(member.name) )
    #else:
    #   print('any')

# Callback when a message is received on channels
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  responses_dict = {
    "$hello" : "Hello!",
    "$i love you" : "i love you too <a:whoaaahh:783617542467092481><a:rainbowdance:810121811899056128> <a:kawaii_lover:810121811777421342> <a:scribbleheart:810121810858213407>",
    "$say gm" : "<a:rainbowdance:810121811899056128> <a:kawaii_lover:810121811777421342> <a:scribbleheart:810121810858213407> Good morning !!<a:scribbleheart:810121810858213407> <a:kawaii_lover:810121811777421342> <a:rainbowdance:810121811899056128>",
    "$say gn" : "<a:rainbowdance:810121811899056128> <a:kawaii_lover:810121811777421342> <a:scribbleheart:810121810858213407> Good night and sweet dreams !!<a:scribbleheart:810121810858213407> <a:kawaii_lover:810121811777421342> <a:rainbowdance:810121811899056128>",
    "$say mi3awa" : "<a:cutecat:806956250181009448> Miaawwwwww miaw <a:cutecat:806956250181009448>",
    "Omi jana" : "ommek 9a7ba" 
  }

  if message.content in responses_dict:
    await message.reply(responses_dict[message.content])

  # Responding to sad comments on /off
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in message.content for word in sad_words):
      await message.reply(random.choice(options))
    if any(word in message.content for word in hachwa_words):
      await message.reply("7alla m3aak <a:scribbleheart:810121810858213407>")

  # New / del commands to add / delete from database    
  if message.content.startswith("$new"):
    encouraging_message = message.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if message.content.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  # Set responding to true/ false
  if message.content.startswith("$responding"):
    value = message.content.split("$responding ",1)[1]

    if value.lower() == "true" or value.lower() == "1":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False or value.lower() == "0"
      db["responding"] = False
      await message.channel.send("Responding is off.")

  # DEBUG AND STUFF
  if message.content.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  #if message.content.startswith("$all_members"):
  #  id = client.get_guild(375641618616811521)
    #await message.channel.send(f"""# of Members: {id.member_count}""")
    
  #  server = message.guild

  #  server_name = server.name
  #  server_id = server.id
    #server_owner = server.owner.name
  #  print(server_name, server_id)
      
    #server = client.get_guild(375641618616811521)
  #  if server:
  #    for member in server.members:
  #      await message.channel.send('name: {}'.format(member.name))
  #      created_at = member.created_at.strftime("%b %d, %Y")
  #      await message.channel.send(created_at)
  #  else:
  #      print('any')
keep_alive()

client.run(os.getenv('TOKEN'))