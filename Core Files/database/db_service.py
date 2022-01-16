from re import search
import psycopg2
from .connect import connect

##################################
#### BASIC INSERTION COMMANDS ####
##################################

def add_game(game_name):
    """ 
    Takes string param 'game_name' and 
    attempts to insert it into the database

    returns 1 if successful
    """
    try:
        conn = connect()
        cursor = conn.cursor()

        ### create the sql statement and sub in
        ### the game name as a lowercase string
        ADD_GAME = """
            INSERT INTO games(game_name)
            VALUES('{}') RETURNING game_id
        """.format(game_name.lower())

        ### insert the row into the table
        cursor.execute(ADD_GAME)

        ### get the created ID and return a success statement
        game_id = cursor.fetchone()[0]
        print("The game has been successfully added with ID of {}".format(game_id))

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            ### close connections so as not to be
            ### a jerk
            cursor.close()
            conn.close()  
            return game_id
        else:
            return None

def add_user(user_name, user_discord_id):
    """ 
    Takes string params 'user_name' and 'user_discord_id' 
    and attempts to insert it into the database
    """
    try:
        conn = connect()
        cursor = conn.cursor()

        ADD_USER = """
            INSERT INTO users(user_name, user_discord_id)
            VALUES ('{0}', '{1}') RETURNING user_id
        """.format(user_name.lower(), user_discord_id)

        cursor.execute(ADD_USER)

        user_id = cursor.fetchone()[0]
        print("The user {0} has been successfully added with ID of {1}".format(user_name, user_id))

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()  
            return user_id
        else:
            return None

def add_group(group_name):
    """ 
    You know what this should do by now...
    """
    try:
        conn = connect()
        cursor = conn.cursor()

        ADD_GROUP = """
            INSERT INTO groups(group_name)
            VALUES ('{0}') RETURNING group_id
        """.format(group_name.lower())

        cursor.execute(ADD_GROUP)

        group_id = cursor.fetchone()[0]
        print("The group {0} has been successfully added with ID of {1}".format(group_name, group_id))

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()  
            return group_id
        else:
            return None


###############################
####### BASIC SEARCHES ########
###############################

def search_user(user_discord_id):
    user = None
    try:
        conn = connect()
        cursor = conn.cursor()

        QUERY = """
        SELECT * FROM users WHERE 
        user_discord_id = '{}'
        """.format(user_discord_id)

        cursor.execute(QUERY)

        user = cursor.fetchone()[0]
        print("User: {}".format(user))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None and user is not None:
            cursor.close()
            conn.close()  
            return user
        else:
            return None


def search_group(group_name):
    group_id = None
    try:
        conn = connect()
        cursor = conn.cursor()

        QUERY = """
        SELECT * FROM groups WHERE 
        group_name = '{}' RETURNING group_id
        """.format(group_name)

        cursor.execute(QUERY)

        group_id = cursor.fetchone()[0]
        print("Group: {}".format(group_id))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None and group_id is not None:
            cursor.close()
            conn.close()  
            return group_id
        else:
            return None


######################################
##### SLIGHTLY LESS BASIC STUFFS #####
######################################

def add_user_to_group(mention, group_id):
    """
    Function to add a user to a group.  If the user
    doesn't exist, it will create a user before adding
    the user to the group.  Takes in a discord 'mention' obj
    and the 'group_id' that you will be adding the user to.
    """
    user_id = search_user(mention.id)
    
    if user_id is None:
        user_id = add_user(mention.name, mention.id)
    
    ### the good stuff
    try:
        conn = connect()
        cursor = conn.cursor()

        ADD_GROUP = """
            INSERT INTO group_users(group_id, user_id)
            VALUES ('{0}', '{1}') RETURNING group_id
        """.format(group_id, user_id)

        cursor.execute(ADD_GROUP)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()  
            return 1
        else:
            return 0