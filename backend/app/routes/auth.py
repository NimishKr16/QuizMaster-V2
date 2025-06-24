from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.admin import Admin

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Admin login
    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.check_password(password):
        token = create_access_token(identity={"role": "admin", "email": admin.email})
        return jsonify(access_token=token), 200

    # User login
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        token = create_access_token(identity={"role": "user", "email": user.email, "id": user.id})
        return jsonify(access_token=token), 200

    return jsonify(msg="Invalid credentials"), 401


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required_fields = ["email", "password", "full_name", "qualification", "dob"]

    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "Email already registered"}), 409

    new_user = User(
        email=data["email"],
        full_name=data["full_name"],
        qualification=data["qualification"],
        dob=data["dob"],
    )
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Registration successful"}), 201