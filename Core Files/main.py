import discord
from pymongo import MongoClient

client = discord.Client()
db_client = MongoClient()

######################
## helper functions ##
######################

### ping a designated user
def ping_user(user_id):
    return "<@{}>".format(user_id)


### round up all mentions into a single array
def list_mentions(message):
    mentions = message.mentions
    requested_users = []

    for mention in mentions:
        requested_users.append(ping_user(mention.id))

    return requested_users





@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    ## author id as var for quick access
    author_id = message.author.id

    ### Greetings
    if message.content.startswith('$hello'):
        await message.channel.send("Hello {}".format(ping_user(author_id)))

    if message.content.startswith('$schedule'):
        requested_users = list_mentions(message)        
        await message.channel.send("Schedule created with requested members. Current party members: {}".format(requested_users))

    if message.content.startswith('$create'):
        requested_users = list_mentions(message)
        await message.channel.send("Created a group with the name: {0}, that includes users: {1}".format("rocket league", requested_users))


client.run('OTMxNjc4NTIyNTQyNTMwNjEx.YeH7PQ.JLrb_FxCnb9iMQp8s49_mZOsmPM')

