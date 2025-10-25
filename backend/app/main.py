# app/main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware  # 👈 added
from .db import init_db, engine
from . import crud, schemas, auth, models
from datetime import timedelta, datetime
from typing import Optional
from sqlmodel import Session

app = FastAPI(title="EventEase API")
init_db()

# 👇 add this block
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", response_model=dict)
def register(user: schemas.UserCreate):
    u = crud.create_user(user.email, user.password)
    return {"id":u.id, "email":u.email}

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate):
    u = crud.authenticate_user(user.email, user.password)
    if not u:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = auth.create_access_token({"sub": str(u.id)})
    return {"access_token": access, "token_type": "bearer"}

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split("Bearer ")[-1]
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    return user_id

@app.get("/events")
def events():
    evs = crud.list_events()
    return [{"id":e.id,"title":e.title,"description":e.description,"date":e.date.isoformat(),"location":e.location,"capacity":e.capacity} for e in evs]

@app.post("/book/{event_id}")
def book(event_id: int, user_id: int = Depends(get_current_user)):
    res = crud.create_booking(user_id, event_id)
    if isinstance(res, dict) and res.get("error"):
        detail = res["error"]
        if detail=="full":
            raise HTTPException(status_code=400, detail="Event full")
        if detail=="already_booked":
            raise HTTPException(status_code=400, detail="Already booked")
        if detail=="event_not_found":
            raise HTTPException(status_code=404, detail="Event not found")
    return {"booking_id": res.booking_id, "event_id": res.event_id, "created_at": res.created_at.isoformat()}

@app.get("/my-bookings")
def my_bookings(user_id: int = Depends(get_current_user)):
    b = crud.get_user_bookings(user_id)
    out = []
    for item in b:
        out.append({"booking_id": item.booking_id, "event_id": item.event_id, "created_at": item.created_at.isoformat()})
    return out

@app.delete("/cancel/{booking_id}")
def cancel(booking_id: str, user_id: int = Depends(get_current_user)):
    res = crud.cancel_booking(user_id, booking_id)
    if isinstance(res, dict) and res.get("error"):
        if res["error"]=="event_started":
            raise HTTPException(status_code=400, detail="Event already started")
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"ok": True}
