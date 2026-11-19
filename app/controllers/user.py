from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import User

bp = Blueprint("user", __name__, url_prefix="/users")


@bp.route("/")
def list_users():
    users = User.query.order_by(User.id).all()
    return render_template("user/list.html", users=users)


@bp.route("/", methods=["POST"])
def create():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()

    if not username or not email:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("user.list_users"))

    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    flash("Usuario creado correctamente.", "success")
    return redirect(url_for("user.list_users"))


@bp.route("/<int:user_id>", methods=["POST"])
def update(user_id):
    user = db.session.get(User, user_id) or abort(404)

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()

    if not username or not email:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("user.list_users"))

    user.username = username
    user.email = email
    db.session.commit()
    flash("Usuario actualizado correctamente.", "success")
    return redirect(url_for("user.list_users"))


@bp.route("/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    user = db.session.get(User, user_id) or abort(404)
    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado.", "success")
    return redirect(url_for("user.list_users"))
