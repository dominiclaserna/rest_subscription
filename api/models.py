from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.String(50), nullable=False)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=True)

    subscriptions = db.relationship("Subscription", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
        }

class Subscription(db.Model):
    __tablename__ = "subscription"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date_subscribed = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    renewed_date = db.Column(db.DateTime)

    product = db.relationship("Product", backref="subscriptions")

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "product_id": self.product_id,
            "status": self.status,
            "date_subscribed": self.date_subscribed.strftime("%Y-%m-%d") if self.date_subscribed else None,
            "end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
            "renewed_date": self.renewed_date.strftime("%Y-%m-%d") if self.renewed_date else None,
        }
