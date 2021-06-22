import sqlite3

connection = sqlite3.connect('business.db')

connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['book', 7.99, 0.5])
connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['drink', 2.00, 0.4])
connection.execute('INSERT INTO products VALUES (?, ?, ?)', ['car', 70000, 1875])

connection.commit()