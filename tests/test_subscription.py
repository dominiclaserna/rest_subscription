import pytest
from myapp import app

@pytest.fixture
def client():
    return app.test_client()

class TestSubscriptionAPI:

    def create_product(self, client):
        client.post("/api/v1/products", json={
            "name": "Premium Service",
            "price": 19.99,
            "frequency": "monthly"
        })

    def create_subscription(self, client):
        self.create_product(client)
        response = client.post("/api/v1/subscriptions", json={
            "user": "user1@example.com",
            "product_id": 1,
            "status": "Subscribed"
        })
        return response.json["id"]

    def test_add_subscription(self, client):
        self.create_product(client)
        response = client.post("/api/v1/subscriptions", json={
            "user": "user1@example.com",
            "product_id": 1,
            "status": "Subscribed"
        })

        assert response.status_code == 201
        assert response.json["user"] == "user1@example.com"
        assert response.json["status"] == "Subscribed"

    def test_view_subscriptions(self, client):
        self.create_subscription(client)
        response = client.get("/api/v1/subscriptions")
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_update_subscription(self, client):
        sub_id = self.create_subscription(client)
        response = client.put(f"/api/v1/subscriptions/{sub_id}", json={
            "user": "user1@example.com",
            "product_id": 1,
            "status": "Unsubscribed"
        })

        assert response.status_code == 200
        assert response.json["msg"] == "updated"

    def test_delete_subscription(self, client):
        sub_id = self.create_subscription(client)
        response = client.delete(f"/api/v1/subscriptions/{sub_id}")
        assert response.status_code == 200
        assert response.json["msg"] == "unsubscribed"

    def test_failed_update(self, client):
        response = client.put("/api/v1/subscriptions/999", json={
            "user": "ghost@example.com",
            "product_id": 999,
            "status": "Subscribed"
        })
        assert response.status_code == 404

    def test_failed_delete(self, client):
        response = client.delete("/api/v1/subscriptions/999")
        assert response.status_code == 404
