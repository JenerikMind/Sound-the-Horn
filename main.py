import discord
import psycopg2
from disc_token import return_token
from database.db_service import add_game, add_user, add_group, add_user_to_group, search_group, build_ping_list, remove_from_group

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

    ### split the message into a handleable array
    message_arr = message.content.split()

    ### create a list of mentions for ease of use
    mentions = list_mentions(message)

    ### Greetings
    if message.content.startswith('$hello'):
        await message.channel.send("Hello {}".format(ping_user(author_id)))

    if message.content.startswith('$schedule'):
        await message.channel.send("Schedule created with requested members. Current party members: {}".format(mentions))


#### CREATE ####
    if message.content.startswith('$create'):
        
        ### get the word immediately after $create
        create_type = message_arr[1].lower()

        if create_type == "game":
            game_name = " ".join(message_arr[2:])
            add_game(game_name)
            await message.channel.send("Added game {} to database".format(game_name))

        if create_type == "user":
            for mention in message.mentions:
                add_user(mention.name, mention.id)
            await message.channel.send("Added user(s) {} to database".format(mentions))

        if create_type == "group":
            group_name = message_arr[2]
            group_id = search_group(group_name) ### check if group exists

            if group_id is None: ### if it doesn't, create one
                group_id = add_group(group_name)

            ### if there are any mentions, add them to the group
            if (message.mentions is not None): 
                for mention in message.mentions:
                    add_user_to_group(mention, group_id) ### semi-baked in user check in add_user_to_group

            await message.channel.send("Added group {} to database".format(group_name))

    
    if message.content.startswith('$remove'):
        ### get the mention.ids
        mention_ids = [mention.id for mention in message.mentions]

        ### get the group name
        group_name_index = message_arr.index("from") ### get the index of the word before the group name
        group_name = message_arr[group_name_index + 1].lower() ### increment by one to get just the group name

        remove_from_group(mention_ids, group_name)
        await message.channel.send("Removed {0} from {1}".format(mentions, group_name))

    
#### SOUND THE HORN! ####
    if message.content.startswith('$assemble') or message.content.startswith('$ring_the_alarm'):
        group_name = message_arr[1]
        broadcast = " ".join(message_arr[2:])

        users = build_ping_list(group_name)
        avengers = [ping_user(user) for user in users]

        await message.channel.send("{0} {1}".format(broadcast, avengers))



client.run(return_token())

