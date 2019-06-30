import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash


from BankManager.db import session_scope, UserClass
from BankManager.error import flash

bp = Blueprint("auth", __name__)

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        with session_scope() as db_session:
            g.user = db_session.query(UserClass) \
                .filter(UserClass.username == user_id).first()

@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        with session_scope() as db_session:
            user = db_session.query(UserClass) \
                .filter(UserClass.username.like(username)).first()
            true_username = user.username
            true_password = user.password

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(true_password, password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = true_username
            return redirect(url_for("bank.bank", page=0))
        return flash(error, "登陆账户", "login.html")

    return render_template("login.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("auth.login", page=0))
