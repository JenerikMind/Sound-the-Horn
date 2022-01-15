import psycopg2
from config import config



def create_tables():
    commands = (
        """
        CREATE TABLE groups (
            group_id SERIAL PRIMARY KEY,
            group_name VARCHAR(80) NOT NULL
        )
        """,
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_discord_id VARCHAR(80) NOT NULL,
            user_name VARCHAR(80)
        )
        """,
        """
        CREATE TABLE games (
            game_id SERIAL PRIMARY KEY,
            game_name VARCHAR(80) NOT NULL
        )
        """,
        """
        CREATE TABLE events (
            event_id SERIAL PRIMARY KEY,
            game_id INTEGER NOT NULL,
            FOREIGN KEY (game_id)
                REFERENCES games (game_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            event_start VARCHAR(80) NOT NULL,
            event_max_participants INTEGER NOT NULL
        )
        """,
        """
        CREATE TABLE event_users (
            event_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (event_id, user_id),
            FOREIGN KEY (event_id)
                REFERENCES events (event_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )

    connection = None
    conn = None
    try:
        # read the connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # create table one by one
        for command in commands:
            cur.execute(command)

        # close communication with the PostgreSQL database server
        cur.close()

        # commit the changes
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()  