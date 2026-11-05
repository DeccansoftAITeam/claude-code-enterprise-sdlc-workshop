import sqlite3
import pytest
from fastapi.testclient import TestClient
import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "DB", tmp_path / "test.db")
    with TestClient(app.app) as client:
        yield client


def headers(token="demo-support", key="key-1"):
    return {"Authorization": f"Bearer {token}", "Idempotency-Key": key, "X-Correlation-ID": "case-123"}


def create(client, amount="500.00", key="key-1", token="demo-support", reason="Customer request", currency="USD", order="order-100"):
    return client.post(f"/orders/{order}/refunds", headers=headers(token, key), json={"amount": amount, "currency": currency, "reason": reason})


def count(table):
    with sqlite3.connect(app.DB) as db:
        return db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]


def test_boundaries_and_fake_effect(client):
    low = create(client)
    high = create(client, "500.01", "key-2")
    assert low.status_code == 201 and low.json()["status"] == "STANDARD_APPROVED"
    assert high.status_code == 202 and high.json()["status"] == "PENDING_FINANCE_APPROVAL"
    assert count("fake_effects") == 1


@pytest.mark.parametrize("amount,currency,reason", [("0", "USD", "x"), ("-1", "USD", "x"), ("1.001", "USD", "x"), (1.5, "USD", "x"), ("1", "EUR", "x"), ("1", "USD", "  ")])
def test_invalid_request_is_audited(client, amount, currency, reason):
    assert create(client, amount, currency=currency, reason=reason).status_code == 422
    assert count("refunds") == 0 and count("audit") == 1


def test_idempotency_replay_conflict(client):
    first = create(client)
    replay = create(client)
    conflict = create(client, "300.00")
    assert replay.status_code == 200 and replay.json()["id"] == first.json()["id"]
    assert conflict.status_code == 409
    assert count("refunds") == 1 and count("fake_effects") == 1 and count("audit") == 3


def test_approval_requires_finance_and_audits_denial(client):
    rid = create(client, "500.01").json()["id"]
    deny = client.post(f"/refunds/{rid}/approval", headers=headers(), json={"decision": "APPROVE", "decision_reason": "valid"})
    assert deny.status_code == 403 and count("fake_effects") == 0
    ok = client.post(f"/refunds/{rid}/approval", headers=headers("demo-finance"), json={"decision": "APPROVE", "decision_reason": "valid"})
    assert ok.status_code == 200 and ok.json()["status"] == "FINANCE_APPROVED"
    assert count("fake_effects") == 1
    assert client.post(f"/refunds/{rid}/approval", headers=headers("demo-finance"), json={"decision": "APPROVE", "decision_reason": "valid"}).status_code == 409
    with sqlite3.connect(app.DB) as db:
        row = db.execute("SELECT actor_id,authorization_result,correlation_id,service_version FROM audit WHERE business_result='forbidden'").fetchone()
        assert row == ("sam", "denied", "case-123", app.VERSION)


def test_reject_and_object_access(client):
    rid = create(client, "800.00").json()["id"]
    result = client.post(f"/refunds/{rid}/approval", headers=headers("demo-finance"), json={"decision": "REJECT", "decision_reason": "not eligible"})
    assert result.json()["status"] == "REJECTED" and count("fake_effects") == 0
    assert client.get(f"/refunds/{rid}", headers=headers("demo-other")).status_code == 403
    assert client.delete("/audit", headers=headers("demo-support")).status_code == 404


def test_missing_invalid_identity_and_order(client):
    assert client.post("/orders/order-100/refunds", json={}).status_code == 401
    assert create(client, token="demo-other").status_code == 403
    assert create(client, order="order-missing").status_code == 404
    assert count("audit") == 3


def test_concurrent_replay_creates_one_refund(client):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: create(client, "100.00", "concurrent-key"), range(2)))
    assert sorted(response.status_code for response in responses) == [200, 201]
    assert responses[0].json()["id"] == responses[1].json()["id"]
    assert count("refunds") == 1 and count("fake_effects") == 1 and count("audit") == 2
