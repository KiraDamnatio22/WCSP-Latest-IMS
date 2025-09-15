import os, sys, sqlite3
from pop_ups.notifs import Toast

def get_app_dir():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.abspath(os.path.dirname(__file__))

def connect_db():
    db_path = os.path.join(get_app_dir(), "test_backend.db")
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    return conn, curr

def insert_to_database(master, *data):
    # for r, x in enumerate(data):
    #     print(f"{r}: {x}")
    conn, curr = connect_db()
    curr.execute("INSERT INTO items (photo, name, category, price, _type, brand, unit, quantity, threshold) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
    conn.commit()
    conn.close()
    Toast(master, "✅ Item Added!", duration=2300)

def retrieve_data():
    conn, curr = connect_db()
    rows = curr.execute("SELECT id, photo, code, name, category, price, _type, brand, unit, quantity, threshold FROM items").fetchall()
    conn.close()
    return rows

def delete_data(master, item_id):
    # print(f"Deleting {item_id}")
    conn, curr = connect_db()
    curr.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    Toast(master, "✅ Item Deleted!", duration=2300)

def update_data(master, item_id, photo_data, new_values):
    # print(item_id, new_values)
    conn, curr = connect_db()

    curr.execute("""
        UPDATE items 
        SET photo = ?, name = ?, category = ?, price = ?, _type = ?, brand = ?, unit = ?, quantity = ?
        WHERE id = ?
    """, (photo_data, *new_values, item_id))

    conn.commit()
    conn.close()
    Toast(master, "✅ Item Updated!", duration=2300)

def create_table():
    conn, curr = connect_db()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT GENERATED ALWAYS AS ( 'C' || printf('%03d', id)) STORED,
            photo BLOB,
            name TEXT,
            category TEXT,
            price REAL,
            _type TEXT,
            brand TEXT,
            unit TEXT,
            quantity INTEGER,
            threshold INTEGER
        )
    ''')

    conn.commit()
    conn.close()
    print("\n Table creation success!")

# create_table()
