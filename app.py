from decimal import Decimal, InvalidOperation
import os
import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Northstar refunds baseline")
DB = Path(os.getenv("NORTHSTAR_DB", "northstar.sqlite3"))

class RefundRequest(BaseModel):
    amount: str

def initialize():
    with sqlite3.connect(DB) as db:
        db.execute("CREATE TABLE IF NOT EXISTS refunds (id INTEGER PRIMARY KEY, order_id TEXT NOT NULL, amount TEXT NOT NULL, status TEXT NOT NULL)")

@app.get("/", response_class=HTMLResponse)
def home():
    return Path(__file__).with_name("index.html").read_text(encoding="utf-8")

@app.post("/orders/{order_id}/refunds", status_code=201)
def create_refund(order_id: str, request: RefundRequest):
    try:
        amount = Decimal(request.amount)
        if not amount.is_finite() or amount <= 0:
            raise ValueError()
    except (InvalidOperation, ValueError):
        raise HTTPException(status_code=422, detail="invalid amount")
    initialize()
    record = {"order_id": order_id, "amount": str(amount), "status": "APPROVED"}
    with sqlite3.connect(DB) as db:
        db.execute("INSERT INTO refunds (order_id, amount, status) VALUES (?, ?, ?)", (order_id, str(amount), "APPROVED"))
    return record
