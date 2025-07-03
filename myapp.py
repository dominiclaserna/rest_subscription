from flask import Flask
from flask_restx import Api
from api.product import product_ns
from api.subscription import subscription_ns

app = Flask(__name__)
api = Api(app, version="1.0", title="Subscription API")

api.add_namespace(subscription_ns, path="/api/v1/subscriptions")
api.add_namespace(product_ns, path="/api/v1/products")

if __name__ == "__main__":
    app.run(debug=True)
