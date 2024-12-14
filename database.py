import sqlite3

def initialize_db():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    ''')
    conn.commit()
    conn.close()

# Добавление товара
def add_item(name, quantity, location):
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, quantity, location) VALUES (?, ?, ?)', (name, quantity, location))
    conn.commit()
    conn.close()

# Получение всех товаров
def get_items():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return items

# Обновление количества товара
def update_item(item_id, quantity):
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET quantity = ? WHERE id = ?', (quantity, item_id))
    conn.commit()
    conn.close()

# Удаление товара
def delete_item(item_id):
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Приёмка товаров
def receive_item(item_id, quantity, date):
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO receipts (item_id, quantity, date) VALUES (?, ?, ?)', (item_id, quantity, date))
    cursor.execute('UPDATE items SET quantity = quantity + ? WHERE id = ?', (quantity, item_id))
    conn.commit()
    conn.close()

# Отгрузка товаров
def ship_item(item_id, quantity, date):
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('SELECT quantity FROM items WHERE id = ?', (item_id,))
    current_quantity = cursor.fetchone()[0]
    if current_quantity >= quantity:
        cursor.execute('INSERT INTO shipments (item_id, quantity, date) VALUES (?, ?, ?)', (item_id, quantity, date))
        cursor.execute('UPDATE items SET quantity = quantity - ? WHERE id = ?', (quantity, item_id))
        conn.commit()
    else:
        raise ValueError("Недостаточно товара для отгрузки")
    conn.close()

# Генерация отчётов
def generate_report():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT items.name, items.quantity, SUM(receipts.quantity) AS total_received, SUM(shipments.quantity) AS total_shipped
        FROM items
        LEFT JOIN receipts ON items.id = receipts.item_id
        LEFT JOIN shipments ON items.id = shipments.item_id
        GROUP BY items.id
    ''')
    report = cursor.fetchall()
    conn.close()
    return report