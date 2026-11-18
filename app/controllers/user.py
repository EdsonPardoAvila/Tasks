from flask import Blueprint, jsonify

from app.models import User

bp = Blueprint("user", __name__, url_prefix="/users")


@bp.route("/")
def list_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])
