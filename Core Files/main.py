import discord
import psycopg2
from tokenize import group
from pprint import pprint
from database.db_service import add_game

client = discord.Client()
conn = psycopg2.connect(
    host="localhost",
    database="sth_test",
    user="postgres",
    password="pgadmin"
)


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

    ### author id as var for quick access
    author_id = message.author.id

    ### Greetings
    if message.content.startswith('$hello'):
        await message.channel.send("Hello {}".format(ping_user(author_id)))

    if message.content.startswith('$schedule'):
        requested_users = list_mentions(message)        
        await message.channel.send("Schedule created with requested members. Current party members: {}".format(requested_users))

    if message.content.startswith('$create'):
        requested_users = list_mentions(message)
        
        ### get the word immediately after $create
        create_type = message.content.split()[1].lower()

        if create_type == "game":
            game_name = " ".join(message.content.split()[2:])
            add_game(game_name)
            await message.channel.send("Added game {} to database".format(game_name))
            
        # groups = db.groups
        # group_details = {
        #     "name": group_name,
        #     "users": requested_users,
        # }

        # result = groups.insert_one(group_details)

        # QueryResult = groups.find_one({"name": group_name})
        # pprint(QueryResult)

        # await message.channel.send("Created a group with the name: {0}, that includes users: {1}".format(group_name, requested_users))


client.run('OTMxNjc4NTIyNTQyNTMwNjEx.YeH7PQ.JLrb_FxCnb9iMQp8s49_mZOsmPM')

