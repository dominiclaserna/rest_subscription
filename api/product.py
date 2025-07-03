from flask_restx import Namespace, Resource, fields

product_ns = Namespace("products", description="Manage Products")

product_model = product_ns.model("Product", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "price": fields.Float(required=True),
})


products = []
product_id_counter = 1

@product_ns.route("")
class ProductList(Resource):
    @product_ns.marshal_list_with(product_model)
    def get(self):
        return products

    @product_ns.expect(product_model)
    @product_ns.marshal_with(product_model, code=201)
    def post(self):
        global product_id_counter
        data = product_ns.payload
        data["id"] = product_id_counter
        products.append(data)
        product_id_counter += 1
        return data, 201
