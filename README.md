# 🎟️ EventEase – Event Booking Platform

EventEase is a full-stack web app built with **Flutter (frontend)** and **FastAPI (backend)** that allows users to browse, book, and manage event registrations.

---

## 🚀 Tech Stack

| Layer | Technology |
|--------|-------------|
| Frontend | Flutter (Web) |
| Backend | FastAPI (Python) |
| Database | SQLite (via SQLModel ORM) |
| Authentication | JWT (via python-jose) |
| Password Hashing | bcrypt (via passlib) |

---

## 🧩 Features

- 🔐 **User Authentication** (Register/Login with JWT)
- 📅 **Browse Events** (Title, Description, Date, Capacity)
- 🪄 **Book Event** (with seat availability check)
- 📜 **View My Bookings**
- ❌ **Cancel Booking** (before event start)
- 🌐 **CORS Enabled** for Flutter web integration

---


---

## ⚙️ Backend Setup (FastAPI)

### 1️⃣ Create virtual environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate


2️⃣ Install dependencies
pip install fastapi uvicorn sqlmodel python-jose passlib[bcrypt]

3️⃣ Run FastAPI server
uvicorn app.main:app --reload --host localhost --port 8000


✅ App runs at: http://localhost:8000

Swagger docs: http://localhost:8000/docs

🖥️ Frontend Setup (Flutter)
1️⃣ Install dependencies
cd frontend/eventease_app
flutter pub get

2️⃣ Run Flutter web app
flutter run -d chrome


App will launch automatically on Chrome:
👉 http://localhost:xxxx

🔌 API Endpoints
Method	Endpoint	Description
POST	/register	Register new user
POST	/login	Login & get JWT token
GET	/events	Get all available events
POST	/book/{event_id}	Book an event
GET	/my-bookings	Get current user bookings
DELETE	/cancel/{booking_id}	Cancel booking
🧪 Testing the API

Use Swagger UI:

Run backend → visit http://localhost:8000/docs

You can register, login, and book events directly from there.

🌱 Sample Data (optional)

You can pre-load some events using a script:

# app/seed_data.py
from sqlmodel import Session
from app.models import Event
from app.db import engine
from datetime import datetime

events = [
    Event(title="Music Fest", description="Live concert", date=datetime(2025, 11, 10, 18, 0), location="Pune", capacity=200),
    Event(title="Tech Conference", description="AI & ML Talks", date=datetime(2025, 12, 5, 10, 0), location="Bangalore", capacity=150),
]

with Session(engine) as s:
    s.add_all(events)
    s.commit()


Then run:

python -m app.seed_data

