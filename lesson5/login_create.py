import sqlite3

connection = sqlite3.connect('users.db')
connection.execute('CREATE TABLE users (username, password)')
