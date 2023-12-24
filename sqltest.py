import mysql.connector

server = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Kolkata1mysql'
)

cursor = server.cursor()

query = 'CREATE DATABASE STREETFIGHTER'
cursor.execute(query)
query = 'USE STREETFIGHTER'
cursor.execute(query)


