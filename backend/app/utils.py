# app/utils.py
import random, string
from datetime import datetime

def gen_booking_id(dt: datetime):
    # format: BKG-[MMM][YYYY]-[Random3]
    mmm = dt.strftime("%b").upper()
    yyyy = dt.strftime("%Y")
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"BKG-{mmm}{yyyy}-{rand}"

def format_dd_mmm_yyyy(dt: datetime):
    return dt.strftime("%d-%b-%Y")  # e.g., 24-Sep-2025
