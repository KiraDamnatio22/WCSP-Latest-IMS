import sqlite3
import os, sys

def get_app_dir():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.abspath(os.path.dirname(__file__))

def connect_db():
    db_path = os.path.join(get_app_dir(), "backend.db")
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    return conn, curr

def retrieve_requests_data():
    conn, curr = connect_db()
    rows = curr.execute("SELECT id, photo, code, name, category, brand, unit, quantity FROM items").fetchall()
    conn.close()
    return rows

def update_item_stock(item_id, new_value):
    print(f"ID: {item_id}, New value: {new_value}, Type: {type(new_value)}")
    conn, curr = connect_db()
    curr.execute("UPDATE items SET quantity = ? WHERE id = ?", (new_value, item_id))
    conn.commit()
    conn.close()
