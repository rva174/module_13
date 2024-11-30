import sqlite3


def add_sample_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.executemany('''
        INSERT INTO Products (title, description, price) VALUES (?, ?, ?)
    ''', [
        ("Яблоко", "Свежие красные яблоки", 50),
        ("Банан", "Спелые бананы", 30),
        ("Апельсин", "Сочные апельсины", 60),
        ("Груша", "Сладкие груши", 70)
    ])
    connection.commit()
    connection.close()

if __name__ == '__main__':
    add_sample_products()