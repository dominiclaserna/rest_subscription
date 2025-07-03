from flask_restx import Namespace, Resource, fields
from flask import request,abort
from .models import db, Product

product_ns = Namespace("products", description="Manage Products")

product_model = product_ns.model("Product", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "price": fields.Float(required=True),
    "frequency": fields.String(required=True, enum=["daily", "weekly", "monthly"]),
})

@product_ns.route("/")
class ProductList(Resource):
    @product_ns.marshal_list_with(product_model)
    def get(self):
        return Product.query.all()
    @product_ns.expect(product_model)
    @product_ns.marshal_with(product_model, code=201)
    def post(self):
        data = request.get_json()

        # price between 10 and 20
        price = data.get("price")
        if price is None:
            abort(400, "Missing price field.")
        if price < 10 or price > 20:
            abort(400, "Price must be between 10 and 20 PHP.")

        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        return new_product, 201

