"""Fictional training service. Demo tokens and local audit are not production security."""
import hashlib
import json
import os
import sqlite3
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

DB = Path(os.getenv("LAB_DB", "northstar.sqlite3"))
VERSION = os.getenv("LAB_VERSION", "2.0-training")
TOKENS = {
    "demo-support": ("sam", "support", {"order-100", "order-missing"}),
    "demo-finance": ("finley", "finance", {"order-100"}),
    "demo-other": ("alex", "support", {"order-200"}),
}


def connect():
    db = sqlite3.connect(DB, timeout=10, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db


def initialize():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY);
        INSERT OR IGNORE INTO orders VALUES ('order-100'), ('order-200');
        CREATE TABLE IF NOT EXISTS refunds (
          id TEXT PRIMARY KEY, order_id TEXT NOT NULL REFERENCES orders(id),
          cents INTEGER NOT NULL, currency TEXT NOT NULL, reason TEXT NOT NULL,
          status TEXT NOT NULL, requested_by TEXT NOT NULL, approved_by TEXT,
          decision_reason TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
          version INTEGER NOT NULL DEFAULT 1, idem_key TEXT NOT NULL UNIQUE,
          fingerprint TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS audit (
          event_id TEXT PRIMARY KEY, actor_id TEXT NOT NULL, action TEXT NOT NULL,
          target_type TEXT NOT NULL, target_id TEXT NOT NULL,
          authorization_result TEXT NOT NULL, business_result TEXT NOT NULL,
          correlation_id TEXT NOT NULL, service_version TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS fake_effects (refund_id TEXT PRIMARY KEY REFERENCES refunds(id));
        """)


@asynccontextmanager
async def lifespan(_app):
    initialize()
    yield


app = FastAPI(title="Northstar training refunds", lifespan=lifespan)


def now():
    return datetime.now(timezone.utc).isoformat()


def actor(request):
    token = request.headers.get("authorization", "").removeprefix("Bearer ")
    return TOKENS.get(token)


def audit(db, who, action, target, authorization, result, correlation):
    db.execute("INSERT INTO audit VALUES (?,?,?,?,?,?,?,?,?,?)", (
        str(uuid.uuid4()), who or "anonymous", action, "refund", target,
        authorization, result, correlation, VERSION, now()))


def reply(payload, status, correlation):
    return JSONResponse(payload, status_code=status, headers={"X-Correlation-ID": correlation})


def public(row):
    return {k: row[k] for k in ("id", "order_id", "cents", "currency", "reason", "status",
                                 "requested_by", "approved_by", "decision_reason", "created_at", "updated_at", "version")}


def money(value):
    # Strings only avoid binary float ambiguity; only exact cents are accepted.
    if not isinstance(value, str):
        raise ValueError("amount must be a decimal string")
    try:
        amount = Decimal(value)
        if not amount.is_finite() or amount <= 0 or amount > Decimal("1000000") or amount.as_tuple().exponent < -2:
            raise ValueError("invalid amount")
        return int(amount * 100)
    except (InvalidOperation, ValueError):
        raise ValueError("invalid amount")


async def body(request):
    try:
        data = await request.json()
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


@app.post("/orders/{order_id}/refunds")
async def create(order_id: str, request: Request):
    correlation = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    user, data = actor(request), await body(request)
    who = user[0] if user else "anonymous"
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        def finish(status, outcome, auth="allowed", result=None):
            audit(db, who, "create", order_id, auth, outcome, correlation)
            db.commit()
            return reply(result or {"detail": outcome}, status, correlation)
        if not user:
            return finish(401, "unauthenticated", "denied")
        if order_id not in user[2]:
            return finish(403, "forbidden", "denied")
        key = request.headers.get("Idempotency-Key", "").strip()
        reason = data.get("reason")
        try:
            cents = money(data.get("amount"))
            if not key or len(key) > 128 or data.get("currency") != "USD" or not isinstance(reason, str) or not reason.strip() or len(reason) > 500:
                raise ValueError("invalid fields")
        except ValueError:
            return finish(422, "invalid request")
        if not db.execute("SELECT 1 FROM orders WHERE id=?", (order_id,)).fetchone():
            return finish(404, "order not found")
        normalized = [order_id, cents, "USD", reason.strip(), who]
        fingerprint = hashlib.sha256(json.dumps(normalized, separators=(",", ":")).encode()).hexdigest()
        old = db.execute("SELECT * FROM refunds WHERE idem_key=?", (key,)).fetchone()
        if old:
            if old["fingerprint"] != fingerprint:
                return finish(409, "idempotency conflict")
            return finish(200, "replay", result=public(old))
        rid, timestamp = str(uuid.uuid4()), now()
        status = "PENDING_FINANCE_APPROVAL" if cents > 50000 else "STANDARD_APPROVED"
        db.execute("INSERT INTO refunds VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            rid, order_id, cents, "USD", reason.strip(), status, who, None, None, timestamp, timestamp, 1, key, fingerprint))
        if status == "STANDARD_APPROVED":
            db.execute("INSERT INTO fake_effects VALUES (?)", (rid,))
        row = db.execute("SELECT * FROM refunds WHERE id=?", (rid,)).fetchone()
        return finish(202 if cents > 50000 else 201, status, result=public(row))


@app.post("/refunds/{refund_id}/approval")
async def approve(refund_id: str, request: Request):
    correlation = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    user, data = actor(request), await body(request)
    who = user[0] if user else "anonymous"
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        def finish(status, outcome, auth="allowed", result=None):
            audit(db, who, "approval", refund_id, auth, outcome, correlation)
            db.commit()
            return reply(result or {"detail": outcome}, status, correlation)
        if not user:
            return finish(401, "unauthenticated", "denied")
        if user[1] != "finance":
            return finish(403, "forbidden", "denied")
        row = db.execute("SELECT * FROM refunds WHERE id=?", (refund_id,)).fetchone()
        if not row:
            return finish(404, "refund not found")
        if row["order_id"] not in user[2]:
            return finish(403, "forbidden", "denied")
        reason, decision = data.get("decision_reason"), data.get("decision")
        if decision not in ("APPROVE", "REJECT") or not isinstance(reason, str) or not reason.strip():
            return finish(422, "invalid decision")
        if row["status"] != "PENDING_FINANCE_APPROVAL":
            return finish(409, "not pending")
        status = "FINANCE_APPROVED" if decision == "APPROVE" else "REJECTED"
        db.execute("UPDATE refunds SET status=?, approved_by=?, decision_reason=?, updated_at=?, version=version+1 WHERE id=?", (status, who, reason.strip(), now(), refund_id))
        if decision == "APPROVE":
            db.execute("INSERT INTO fake_effects VALUES (?)", (refund_id,))
        row = db.execute("SELECT * FROM refunds WHERE id=?", (refund_id,)).fetchone()
        return finish(200, status, result=public(row))


@app.get("/refunds/{refund_id}")
def get_refund(refund_id: str, request: Request):
    correlation = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    user = actor(request)
    if not user:
        return reply({"detail": "unauthenticated"}, 401, correlation)
    with connect() as db:
        row = db.execute("SELECT * FROM refunds WHERE id=?", (refund_id,)).fetchone()
        if not row:
            return reply({"detail": "refund not found"}, 404, correlation)
        if row["order_id"] not in user[2]:
            return reply({"detail": "forbidden"}, 403, correlation)
        return reply(public(row), 200, correlation)


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return Path(__file__).with_name("review.html").read_text(encoding="utf-8")
