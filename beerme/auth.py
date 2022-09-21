import functools
from ipaddress import ip_address
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from beerme.db import get_db

# DEFINING THE BLUEPRINT CALLED `auth`
bp = Blueprint("auth", __name__, url_prefix="/")

# CREATING A register VIEW THAT IS REGISTERED TO THE `auth` BLUEPRINT
@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ip_address = request.remote_addr
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, user_ip) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), ip_address),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


# LOGIN VIEW THAT IS REGISTERED TO THE `AUTH` BLUEPRINT
@bp.route("/", methods=("GET", "POST"))
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE USERNAME = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("checkin.log_beer"))

        flash(error)

    return render_template("auth/login.html")


# FUNCTION TO CHECK IF USER IS LOGGED INTO SESSION BEFORE ANY REQUEST
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE ID = ?", (user_id,)).fetchone()
        )


# LOGOUT VIEW REGISTERED TO AUTH BLUEPRINT
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# REQUIRE AUTHENTICATION IN OTHER VIEWS
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view