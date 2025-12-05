import sqlite3
import os
import json


DB_FILE = 'project.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS users (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           email TEXT NOT NULL
                           )
                       ''')

        conn.commit()


def get_all_users():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]

def add_user(username, email):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
        return cursor.lastrowid

def update_user(user_id, username, email):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            return False
        
        cursor.execute("UPDATE users SET username = ?, email = ? WHERE id = ?", (username, email, user_id))
        conn.commit()
        return True




init_db()
