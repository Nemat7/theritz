from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import logging
from .telegram_bot import send_telegram_notification
from .database import save_booking

app = FastAPI(title="THE RITZ Booking API")

# CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
 )

class BookingRequest(BaseModel):
    name: str
    phone: str
    date: str
    time: str
    guests: int
    comments: str = None


@app.post("/api/booking")
async def create_booking(booking: BookingRequest):
    try:
        # Валидация данных
        if not booking.name or not booking.phone:
            raise HTTPException(status_code=400, detail="Name and phone are required")

        # Сохраняем в базу
        booking_id = save_booking(booking)

        # Отправляем в Телешрам
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