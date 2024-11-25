# ДЗ "Создание БД, добавление, выбор и удаление элементов"
# ДЗ "Создание БД, добавление, выбор и удаление элементов"
# Задача "Первые пользователи"

import sqlite3
#import random

import os
# Удаляем базу данных "not_telegram.db", если она уже есть
if os.path.exists("not_telegram.db"):
    os.remove("not_telegram.db")

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")
for i in range(10):
    age = 10 * (i + 1)
    cursor.execute( "INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                    (f"newuser{i+1}", f"example{i+1}@gmail.com", age, 1000))

# Обновление balance у каждой 2-й записи, начиная с 1-й
cursor.execute("UPDATE Users SET balance = balance - 500 WHERE id % 2 = 1")

# Удаление каждой 3-й записи, начиная с 1-й
cursor.execute("DELETE FROM Users WHERE id % 3 = 1")

# Выборка  FROM Users WHERE age != 60"
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
results = cursor.fetchall()


for row in results:
    username, email, age, balance = row
    print(f"Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}")

connection.commit()
connection.close()