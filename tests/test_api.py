import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import uuid
import pytest
from flask import Flask
from api.models import db
from api.user import user_ns
from api.product import product_ns
from api.subscription import subscription_ns
from flask_restx import Api


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    db.init_app(app)
    api = Api(app)
    api.add_namespace(user_ns, path="/users")
    api.add_namespace(product_ns, path="/products")
    api.add_namespace(subscription_ns, path="/subscriptions")

    with app.app_context():
        db.create_all()
    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def generate_unique_email():
    return f"user_{uuid.uuid4()}@example.com"


class TestAPI:

    def create_user(self, client):
        email = generate_unique_email()
        response = client.post("/users/", json={
            "username": email,
            "email": email,
            "phone": "09123456789"
        })
        assert response.status_code == 201
        data = response.get_json()
        return data["id"], email

    def create_product(self, client):
        response = client.post("/products/", json={
            "name": "Spotify",
            "price": 15.0,
            "frequency": "monthly"
        })
        assert response.status_code == 201
        data = response.get_json()
        return data["id"]

    def test_add_product(self, client):
        response = client.post("/products/", json={
            "name": "Netflix",
            "price": 17.5,
            "frequency": "weekly"
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Netflix"
        assert data["price"] == 17.5
        assert data["frequency"] == "weekly"

    def test_view_products(self, client):
        self.create_product(client)
        response = client.get("/products/")
        assert response.status_code == 200
        products = response.get_json()
        assert isinstance(products, list)
        assert all("name" in p for p in products)

    def test_add_subscription(self, client):
        user_id, username = self.create_user(client)
        product_id = self.create_product(client)

        response = client.post("/subscriptions/", json={
            "username": username,
            "product_id": product_id,
            "status": "Subscribed"
        })

        assert response.status_code == 201
        data = response.get_json()
        assert data["user"] == username
        assert data["product_id"] == product_id
        assert data["status"] == "Subscribed"

    def test_view_subscriptions(self, client):
        user_id, username = self.create_user(client)
        product_id = self.create_product(client)

        # Create a subscription
        client.post("/subscriptions/", json={
            "username": username,
            "product_id": product_id,
            "status": "Subscribed"
        })

        # Retrieve list
        response = client.get("/subscriptions/")
        assert response.status_code == 200
        subs = response.get_json()
        assert isinstance(subs, list)
        assert any(sub["user"] == username for sub in subs)
