from settings import *


def setup_mysql():
    import mysql.connector
    game_server = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = SQL_PASS,
    )

    return [game_server, game_server.cursor()]

def load_client_data():
    server_ops = setup_mysql()
    game_server = server_ops[0]
    server_cursor = server_ops[1]
    try:
        server_cursor.execute(
            'USE STREETFIGHTER'
        )
    except:
        server_cursor.execute(
            'CREATE DATABASE STREETFIGHTER'
        )
        server_cursor.execute(
            'USE STREETFIGHTER'
        )

    try:
        server_cursor.execute(
            'SELECT * FROM GAME_DATA'
        )
        game_data = server_cursor.fetchall()
    except:
        server_cursor.execute(
            'CREATE TABLE GAME_DATA(playername varchar(30), attack int, defense int, coins int)'
        )
        server_cursor.execute(
            f"INSERT INTO GAME_DATA VALUES('RYU', {BASE_STATS['attack']}, {BASE_STATS['defense']}, 250)"
        )
        game_server.commit()
        server_cursor.execute(
            'SELECT * FROM GAME_DATA'
        )
        game_data = server_cursor.fetchall()
    print(game_data)

    game_server.close()
    

    return game_data[0]

def save_client_data(data):
    server_ops = setup_mysql()
    game_server = server_ops[0]
    server_cursor = server_ops[1]

    server_cursor.execute("USE streetfighter")
    server_cursor.execute(
        f"UPDATE game_data SET attack = {data[0]}, defense = {data[1]}, coins = {data[2]}"
    )
    game_server.commit()