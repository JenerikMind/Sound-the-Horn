import psycopg2
from .connect import connect


def add_game(game_name):
    """ 
    Takes string param 'game_name' and 
    attempts to insert it into the database
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
