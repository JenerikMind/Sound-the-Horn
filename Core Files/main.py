import discord
import psycopg2
from tokenize import group
from pprint import pprint
from database.db_service import add_game, add_user, add_group, add_user_to_group, search_group, build_ping_list

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


#### CREATE ####
    if message.content.startswith('$create'):
        requested_users = list_mentions(message)
        
        ### get the word immediately after $create
        create_type = message.content.split()[1].lower()

        if create_type == "game":
            game_name = " ".join(message.content.split()[2:])
            add_game(game_name)
            await message.channel.send("Added game {} to database".format(game_name))

        if create_type == "user":
            for mention in message.mentions:
                add_user(mention.name, mention.id)
            await message.channel.send("Added user(s) {} to database".format(requested_users))

        if create_type == "group":
            group_name = message.content.split()[2]
            group_id = search_group(group_name) ### check if group exists

            if group_id is None: ### if it doesn't, create one
                group_id = add_group(group_name)

            ### if there are any mentions, add them to the group
            if (message.mentions is not None): 
                for mention in message.mentions:
                    add_user_to_group(mention, group_id) ### semi-baked in user check in add_user_to_group

            await message.channel.send("Added group {} to database".format(group_name))

    
#### SOUND THE HORN! ####
    if message.content.startswith('$Assemble') or message.content.startswith('$ring_the_alarm'):
        message_arr = message.content.split()
        group_name = message_arr[1]
        broadcast = " ".join(message_arr[2:])

        users = build_ping_list(group_name)
        avengers = [ping_user(user) for user in users]

        await message.channel.send("{0} {1}".format(broadcast, avengers))



client.run('OTMxNjc4NTIyNTQyNTMwNjEx.YeH7PQ.JLrb_FxCnb9iMQp8s49_mZOsmPM')

