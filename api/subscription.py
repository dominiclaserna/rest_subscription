from flask_restx import Namespace, Resource, fields, abort
from flask import request
from datetime import datetime, timedelta
from .models import db, Subscription, Product, User

subscription_ns = Namespace("subscriptions", description="Manage Subscriptions")

subscription_model = subscription_ns.model("Subscription", {
    "id": fields.Integer(readonly=True),
    "user": fields.String(required=True, description="Username, phone, or email"),
    "product_id": fields.Integer(required=True),
    "status": fields.String(required=True, enum=["Subscribed", "Unsubscribed"]),
    "date_subscribed": fields.String(readonly=True),
    "end_date": fields.String(readonly=True),
    "renewed_date": fields.String(readonly=True),
})

def get_duration_by_frequency(freq):
    if freq == "daily":
        return timedelta(days=1)
    elif freq == "weekly":
        return timedelta(weeks=1)
    elif freq == "monthly":
        return timedelta(days=30)
    return timedelta(days=0)

@subscription_ns.route("")
class SubscriptionList(Resource):
    @subscription_ns.marshal_list_with(subscription_model)
    def get(self):
        return Subscription.query.all()

    @subscription_ns.expect(subscription_model)
    @subscription_ns.marshal_with(subscription_model, code=201)
    def post(self):
        data = request.get_json()

   
        username = data.get("username")
        if not username:
            abort(400, "Missing username.")

        #Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(400, f"User '{username}' does not exist.")

        product = Product.query.get(data["product_id"])
        if not product:
            abort(400, "Product does not exist.")

        duration = get_duration_by_frequency(product.frequency)
        now = datetime.now()

        new_sub = Subscription(
            user_id=user.id,
            product_id=data["product_id"],
            status=data["status"],
            date_subscribed=now,
            end_date=(now + duration),
            renewed_date=None
        )

        db.session.add(new_sub)
        db.session.commit()
        return new_sub, 201

@subscription_ns.route("/<int:id>")
class SubscriptionResource(Resource):
    @subscription_ns.expect(subscription_model)
    def put(self, id):
        sub = Subscription.query.get(id)
        if not sub:
            abort(404, "Subscription not found")

        data = request.get_json()
        for field in ["user", "product_id"]:
            if not data.get(field):
                abort(400, f"Missing field: {field}")

        product = Product.query.get(data["product_id"])
        if not product:
            abort(400, "Product no longer exists")

        duration = get_duration_by_frequency(product.frequency)
        now = datetime.now()

        sub.user = data["user"]
        sub.product_id = data["product_id"]
        sub.status = "Subscribed"
        sub.renewed_date = now.strftime("%Y-%m-%d")
        sub.end_date = (now + duration).strftime("%Y-%m-%d")

        db.session.commit()
        return {"msg": "updated"}, 200

    def delete(self, id):
        sub = Subscription.query.get(id)
        if not sub:
            abort(404, "Subscription not found")

        db.session.delete(sub)
        db.session.commit()
        return {"msg": "unsubscribed"}, 200
