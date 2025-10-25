# app/crud.py
from sqlmodel import Session, select
from .models import User, Event, Booking
from .db import engine
from .auth import hash_password, verify_password
from .utils import gen_booking_id
from datetime import datetime

def create_user(email, password):
    with Session(engine) as s:
        user = User(email=email, hashed_password=hash_password(password))
        s.add(user); s.commit(); s.refresh(user)
        return user

def authenticate_user(email, password):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.email==email)).first()
        if not user: return None
        if not verify_password(password, user.hashed_password): return None
        return user

def list_events():
    with Session(engine) as s:
        events = s.exec(select(Event).order_by(Event.date)).all()
        return events

def get_event(eid):
    with Session(engine) as s:
        return s.get(Event, eid)

def count_bookings_for_event(eid):
    with Session(engine) as s:
        return s.exec(select(Booking).where(Booking.event_id==eid)).count()

def user_has_booking_for_event(uid, eid):
    with Session(engine) as s:
        return s.exec(select(Booking).where(Booking.user_id==uid, Booking.event_id==eid)).first() is not None

def create_booking(user_id, event_id):
    with Session(engine) as s:
        event = s.get(Event, event_id)
        if not event:
            return {"error":"event_not_found"}
        # capacity check
        booked = s.exec(select(Booking).where(Booking.event_id==event_id)).count()
        if booked >= event.capacity:
            return {"error":"full"}
        # single seat per user
        exists = s.exec(select(Booking).where(Booking.event_id==event_id, Booking.user_id==user_id)).first()
        if exists:
            return {"error":"already_booked"}
        # create booking
        bkg_id = gen_booking_id(datetime.utcnow())
        booking = Booking(booking_id=bkg_id, user_id=user_id, event_id=event_id)
        s.add(booking)
        s.commit(); s.refresh(booking)
        # log
        print(f"New booking: user={user_id} booking_id={bkg_id} at {booking.created_at}")
        return booking

def get_user_bookings(user_id):
    with Session(engine) as s:
        return s.exec(select(Booking).where(Booking.user_id==user_id)).all()

def cancel_booking(user_id, booking_id):
    with Session(engine) as s:
        booking = s.exec(select(Booking).where(Booking.booking_id==booking_id, Booking.user_id==user_id)).first()
        if not booking:
            return {"error":"not_found"}
        # check event hasn't started
        event = s.get(Event, booking.event_id)
        if event.date <= datetime.utcnow():
            return {"error":"event_started"}
        s.delete(booking)
        s.commit()
        return {"ok":True}
