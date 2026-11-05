from fastapi.testclient import TestClient
import app


def test_existing_path_approves_high_value(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "DB", tmp_path / "baseline.sqlite3")
    with TestClient(app.app) as client:
        response = client.post('/orders/order-100/refunds', json={'amount': '501.00'})
    assert response.status_code == 201
    assert response.json()['status'] == 'APPROVED'
