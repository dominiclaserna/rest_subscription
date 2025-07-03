import pytest
from myapp import app

@pytest.fixture
def client():
    return app.test_client()

class TestSubscriptionAPI:

    def test_add_subscription(self, client):
        # First, add a product to subscribe to
        client.post("/api/v1/products", json={"name": "Premium Service"})

        response = client.post("/api/v1/subscriptions", json={
            "user": "user1",
            "product_id": 1,
            "status": "Subscribed"
        })

        assert response.status_code == 201
        assert response.json["user"] == "user1"
        assert response.json["status"] == "Subscribed"

    def test_view_subscriptions(self, client):
        response = client.get("/api/v1/subscriptions")
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_update_subscription(self, client):
        response = client.put("/api/v1/subscriptions/1", json={
            "user": "user1",
            "product_id": 1,
            "status": "Unsubscribed"
        })

        assert response.status_code == 200
        assert response.json["msg"] == "updated"

    def test_delete_subscription(self, client):
        response = client.delete("/api/v1/subscriptions/1")
        assert response.status_code == 200
        assert response.json["msg"] == "unsubscribed"

    def test_failed_update(self, client):
        response = client.put("/api/v1/subscriptions/999", json={
            "user": "ghost",
            "product_id": 999,
            "status": "Subscribed"
        })

        assert response.status_code == 404

    def test_failed_delete(self, client):
        response = client.delete("/api/v1/subscriptions/999")
        assert response.status_code == 404
