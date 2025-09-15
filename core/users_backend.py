import sqlite3
import os, sys

def get_app_dir():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.abspath(os.path.dirname(__file__))

def connect_db():
    db_path = os.path.join(get_app_dir(), "users_db.db")
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    return conn, curr

def create_table():
    conn, curr = connect_db()
    curr.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT,
            photo BLOB
        ) 
    """)
    conn.commit()
    conn.close()
    print("\n Table created.")

def insert_new_user(first_name, last_name, username, password, role, photo):
    conn, curr = connect_db()
    curr.execute("""
        INSERT INTO users (firstname, lastname, username, password, role, photo) VALUES (?, ?, ?, ?, ?, ?)""", 
        (first_name, last_name, username, password, role, photo)),

    employee_id = curr.lastrowid
    product_code = f"WCSPE{employee_id:03d}"

    curr.execute("UPDATE users SET code = ? WHERE id = ?", (product_code, employee_id))
    conn.commit()
    conn.close()
    print("\n New user registered.")
    return product_code

def retrieve_all_user_data():
    conn, curr = connect_db()
    rows = curr.execute("SELECT id, photo, code, firstname, lastname, username, role FROM users").fetchall()
    conn.close()
    return rows

# retrieve_all_user_data()

def retrieve_user_data(item_id):
    conn, curr = connect_db()
    rows = curr.execute("SELECT * FROM users WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return rows

def retrieve_user_data_by_name(username):
    conn, curr = connect_db()
    account = curr.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return account

def delete_user(item_id):
    print(f"Deleting {item_id, type(item_id)}")
    conn, curr = connect_db()
    curr.execute("DELETE FROM users WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def update_first_name(user_id, new_first_name):
    conn, curr = connect_db()
    curr.execute("UPDATE users SET firstname = ? WHERE id = ?", (new_first_name, user_id))
    conn.commit()
    conn.close()

def update_last_name(user_id, new_last_name):
    conn, curr = connect_db()
    curr.execute("UPDATE users SET lastname = ? WHERE id = ?", (new_last_name, user_id))
    conn.commit()
    conn.close()

def update_username(user_id, new_username):
    conn, curr = connect_db()
    curr.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
    conn.commit()
    conn.close()

def update_password(user_id, new_password):
    conn, curr = connect_db()
    curr.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()

def update_role(user_id, new_role):
    conn, curr = connect_db()
    curr.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()

def remove_entire_db_table():
    conn, curr = connect_db()
    curr.execute("DROP TABLE IF EXISTS users;")
    conn.commit()
    conn.close()
    print("\n\n Table removed.")


'''Create the table'''
# create_table()

'''Delete the table'''
# remove_entire_db_table()

'''Test methods'''
# insert_new_user("admin", "123", "admin")
# retrieve_user_data(1)
