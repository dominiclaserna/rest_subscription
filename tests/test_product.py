import pytest
from myapp import app

@pytest.fixture
def client():
    return app.test_client()

class TestProductAPI:

    def test_add_product(self, client):
        response = client.post(
            "/api/v1/products",
            json={
                "name": "Spotify",
                "price": 15.0,
                "frequency": "monthly"
            }
        )
        assert response.status_code == 201
        assert response.json["name"] == "Spotify"
        assert response.json["price"] == 15.0
        assert response.json["frequency"] == "monthly"

    def test_view_products(self, client):
        response = client.get("/api/v1/products")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert all("name" in product for product in response.json)
        assert all("price" in product for product in response.json)
        assert all("frequency" in product for product in response.json)
