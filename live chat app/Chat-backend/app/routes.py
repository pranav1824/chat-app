# app/routes.py
from flask import Blueprint, request, jsonify
from . import db
from .models import User, Message
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flask import Blueprint, jsonify
from app.models import Message

bp = Blueprint("main", __name__)

# bp = Blueprint('main', __name__)

@bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    data = [
        {'username': m.username, 'message': m.message, 'timestamp': m.timestamp.isoformat()}
        for m in messages
    ]
    return jsonify(data)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "username already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "user created", "user": user.to_dict()}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"msg": "bad username or password"}), 401

    additional_claims = {"role": user.role}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200

# Example protected endpoint: fetch recent messages
@bp.route("/chat/messages", methods=["GET"])
@jwt_required()
def get_messages():
    # return last 50 messages
    msgs = Message.query.order_by(Message.timestamp.desc()).limit(50).all()
    return jsonify([m.to_dict() for m in reversed(msgs)])  # oldest first

# Admin only example
@bp.route("/admin/users", methods=["GET"])
@jwt_required()
def admin_get_users():
    claims = request.environ.get("flask_jwt_extended").get("jwt") if False else None
    # safer: use get_jwt to access claims (but keep compatibility):
    from flask_jwt_extended import get_jwt
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"msg": "admin access required"}), 403

    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
