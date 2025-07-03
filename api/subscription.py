from flask_restx import Namespace, Resource, fields, abort

subscription_ns = Namespace("subscriptions", description="Manage Subscriptions")

subscription_model = subscription_ns.model("Subscription", {
    "id": fields.Integer(readonly=True),
    "user": fields.String(required=True),
    "product_id": fields.Integer(required=True),
    "status": fields.String(required=True, enum=["Subscribed", "Unsubscribed"]),
})

subscriptions = []
subscription_id_counter = 1

def validate_subscription_payload(data):
    required_fields = ["user", "product_id", "status"]
    missing = [field for field in required_fields if field not in data or data[field] in (None, "")]
    if missing:
        abort(400, f"Missing or empty fields: {', '.join(missing)}")
    if data["status"] not in ["Subscribed", "Unsubscribed"]:
        abort(400, "Invalid status. Must be 'Subscribed' or 'Unsubscribed'")

@subscription_ns.route("")
class SubscriptionList(Resource):
    @subscription_ns.marshal_list_with(subscription_model)
    def get(self):
        return subscriptions

    @subscription_ns.expect(subscription_model)
    @subscription_ns.marshal_with(subscription_model, code=201)
    def post(self):
        global subscription_id_counter
        data = subscription_ns.payload

        validate_subscription_payload(data)

        new_subscription = {
            "id": subscription_id_counter,
            "user": data["user"],
            "product_id": data["product_id"],
            "status": data["status"],
        }

        subscriptions.append(new_subscription)
        subscription_id_counter += 1
        return new_subscription, 201

@subscription_ns.route("/<int:id>")
class Subscription(Resource):
    @subscription_ns.expect(subscription_model)
    def put(self, id):
        data = subscription_ns.payload
        validate_subscription_payload(data)

        for sub in subscriptions:
            if sub["id"] == id:
                sub["user"] = data["user"]
                sub["product_id"] = data["product_id"]
                sub["status"] = data["status"]
                return {"msg": "updated"}, 200

        abort(404, "Subscription not found")

    def delete(self, id):
        for i, sub in enumerate(subscriptions):
            if sub["id"] == id:
                subscriptions.pop(i)
                return {"msg": "unsubscribed"}, 200
        abort(404, "Subscription not found")
