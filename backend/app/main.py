from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import logging
import sqlite3
import requests
import os
from typing import Optional

# Инициализация FastAPI
app = FastAPI(title="THE RITZ Booking API")

# CORS для работы с фронтендом - ОБНОВЛЕНО!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все origins для тестирования
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)



# Модель данных для бронирования
class BookingRequest(BaseModel):
    name: str
    phone: str
    date: str
    time: str
    guests: int
    comments: str = None


# Конфигурация базы данных
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


# Telegram функция
def send_telegram_notification(message: str) -> bool:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    print(f"Telegram Token: {TELEGRAM_BOT_TOKEN}")
    print(f"Telegram Chat ID: {TELEGRAM_CHAT_ID}")

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not set")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Telegram response: {response.status_code}")
        print(f"Telegram response text: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram send error: {e}")
        return False


def format_telegram_message(booking: BookingRequest) -> str:
    return f"""
🎉 НОВАЯ БРОНЬ THE RITZ
—————————————
👤 Имя: {booking.name}
📞 Телефон: {booking.phone}
🗓 Дата: {booking.date}
🕐 Время: {booking.time}
👥 Гости: {booking.guests} чел.
💬 Комментарий: {booking.comments or 'нет'}
—————————————
⏰ Время заявки: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""


# Инициализация базы данных при старте
init_db()


@app.get("/")
async def root():
    return {"message": "THE RITZ Booking API is running"}


@app.post("/api/booking")
async def create_booking(booking: BookingRequest):
    try:
        # Валидация данных
        if not booking.name or not booking.phone:
            raise HTTPException(status_code=400, detail="Name and phone are required")

        # Сохраняем в базу
        booking_id = save_booking(booking)

        # Отправляем в Telegram
        message = format_telegram_message(booking)
        send_telegram_notification(message)

        return {
            "success": True,
            "booking_id": booking_id,
            "message": "Бронь успешно создана"
        }

    except Exception as e:
        logging.error(f"Booking error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/bookings")
async def get_bookings():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")
        bookings = cursor.fetchall()
        conn.close()

        return {"bookings": bookings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))