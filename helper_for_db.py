import csv
import sqlite3

# Создание базы данных SQLite
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Создание таблицы books
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        category TEXT,
        century TEXT,
        country TEXT
    )
''')
conn.commit()

# Заполнение таблицы из CSV файла
with open('book.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
            INSERT INTO books (title, genre, category, century, country)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['title'], row['genre'], row['category'], row['century'], row['country']))
    conn.commit()

# Закрытие соединения с базой данных
conn.close()
