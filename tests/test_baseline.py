from fastapi.testclient import TestClient
from app import app


def test_existing_path_approves_high_value():
    with TestClient(app) as client:
        response = client.post('/orders/order-100/refunds', json={'amount': '501.00'})
    assert response.status_code == 201
    assert response.json()['status'] == 'APPROVED'
