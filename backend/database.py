import sqlite3
import os
from datetime import datetime

DB_PATH = "bookings.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            guests INTEGER NOT NULL,
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'new'
        )
        """)

    conn.commit()
    conn.close()

def save_booking(booking) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings (name, phone, date, time, guests, comments)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (booking.name, booking.phone, booking.date, booking.time, booking.guests, booking.comments))

    booking_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return booking_id