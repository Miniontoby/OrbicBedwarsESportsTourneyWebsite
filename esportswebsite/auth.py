"""Authentication blueprint"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(user_type=None):
    """View decorator that redirects anonymous users to the login page."""
    def func(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if (
                (user_type is None and g.user is None and g.team is None)
                or (user_type == "team" and g.team is None)
                or (user_type == "user" and g.user is None)
            ):
                return redirect(url_for("auth.login"))

            return view(**kwargs)

        return wrapped_view
    return func


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""

    db = get_db()
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        user_obj = db.execute(
            "SELECT id, username FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        g.user = user_obj

    team_id = session.get("team_id")
    if team_id is None:
        g.team = None
    else:
        team_obj = db.execute(
            "SELECT id, username FROM team WHERE id = ?", (team_id,)
        ).fetchone()
        g.team = team_obj


@bp.route("/register", methods=("GET", "POST"))
@login_required("user") # Only allow admins to register new users...
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT id, password FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password"], password):
            error = "Incorrect username or password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        error = None # Reset error, since it might not be a user, but just a team login...

        team = db.execute(
            "SELECT id, password FROM team WHERE username = ?", (username,)
        ).fetchone()

        if team is None or not check_password_hash(team["password"], password):
            error = "Incorrect username or password."

        if error is None:
            # store the team id in a new session and return to the index
            session.clear()
            session["team_id"] = team["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
