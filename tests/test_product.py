import pytest
from myapp import app

@pytest.fixture
def client():
    return app.test_client()

class TestProductAPI:

    def test_add_product(self, client):
        response = client.post("/api/v1/products", json={"name": "Pro Plan"})
        assert response.status_code == 201
        assert response.json["name"] == "Pro Plan"

    def test_view_products(self, client):
        response = client.get("/api/v1/products")
        assert response.status_code == 200
        assert isinstance(response.json, list)
