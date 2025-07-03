from flask_restx import Namespace, Resource, fields
from flask import request, abort
from .models import db, User

user_ns = Namespace("users", description="Manage Users")

user_model = user_ns.model("User", {
    "id": fields.Integer(readonly=True),
    "username": fields.String(required=True, description="Unique username"),
    "email": fields.String(description="User email address"),
    "phone": fields.String(description="User phone number"),
})

@user_ns.route("")
class UserList(Resource):
    @user_ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        data = request.get_json()

        existing = User.query.filter_by(username=data["username"]).first()
        if existing:
            abort(400, f"Username '{data['username']}' already exists.")

        user = User(
            username=data["username"],
            email=data.get("email"),
            phone=data.get("phone")
        )
        db.session.add(user)
        db.session.commit()
        return user, 201

@user_ns.route("/<int:id>")
class UserResource(Resource):
    @user_ns.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, "User not found.")
        return user

    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model)
    def put(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, "User not found.")
        
        data = request.get_json()
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.phone = data.get("phone", user.phone)
        db.session.commit()
        return user

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, "User not found.")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
