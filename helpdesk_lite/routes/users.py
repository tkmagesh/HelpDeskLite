from flask import Blueprint, flash, redirect, render_template, request, url_for

from helpdesk_lite.services.user_service import UserService


users_bp = Blueprint("users", __name__, url_prefix="/users")
user_service = UserService()


@users_bp.get("/")
def list_users():
    users = user_service.list_users()
    return render_template("users/list.html", users=users)


@users_bp.route("/new", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        user, errors = user_service.create_user(
            request.form.get("name", ""), request.form.get("email", "")
        )
        if not errors:
            flash(f"Created user {user.name}.", "success")
            return redirect(url_for("users.list_users"))

        for error in errors:
            flash(error, "error")

    return render_template("users/new.html")
