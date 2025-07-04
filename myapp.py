import os
from flask import Flask, jsonify
from flask_restx import Api
from sqlalchemy import inspect
from api.models import db, User,Product, Subscription
from api.product import product_ns
from api.subscription import subscription_ns
from api.user import user_ns

def create_app():
    app = Flask(__name__)

    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app, version="1.0", title="Subscription API", prefix="/api/v1")
    api.add_namespace(product_ns)
    api.add_namespace(subscription_ns)
    api.add_namespace(user_ns)   

    with app.app_context():
        db.create_all()
        print("✅ DB file should be created at:", db_path)

    @app.route("/debug/tables")
    def show_tables():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        return jsonify({"tables": tables})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
