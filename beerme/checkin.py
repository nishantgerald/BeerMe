import functools
from datetime import datetime
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
from beerme.auth import login_required
import pandas as pd
import hashlib

brewery_df=pd.read_csv('beerme/data/brewery.csv', on_bad_lines='skip')[['name']]
brewery_list = brewery_df.name.to_list()

# DEFINING THE BLUEPRINT CALLED `checkin`
bp = Blueprint("checkin", __name__, url_prefix="/checkin")

# DEFINING THE log_beer VIEW AND REGISTERING IT WITH THE checkin BLUEPRINT
@bp.route("/", methods=("GET", "POST"))
@bp.route("/log_beer", methods=("GET", "POST"))
@login_required
def log_beer():
    if request.method == "POST":
        BEER_NAME = request.form["BEER_NAME"].lower()
        BEER_TYPE = request.form["BEER_TYPE"].lower()
        BREWERY_NAME = request.form["BREWERY_NAME"].lower()
        BEER_RATING = request.form["BEER_RATING"]
        USERNAME = g.user['username']
        PRECODED_CHECKIN_ID = BEER_NAME + BREWERY_NAME + USERNAME
        CHECKIN_ID = hashlib.md5(PRECODED_CHECKIN_ID.encode('utf-8')).hexdigest()

        db = get_db()
        error = None

        if not BEER_NAME:
            error = "Beer name is required."
        elif not BREWERY_NAME:
            error = "Brewery name is required."
        elif not BEER_RATING:
            error = "Rating is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO beers (CHECKIN_ID, USERNAME, BEER_NAME, BEER_TYPE, BREWERY_NAME, BEER_RATING) VALUES (?, ?, ?, ?, ?, ?)",
                    (CHECKIN_ID, USERNAME, BEER_NAME, BEER_TYPE, BREWERY_NAME, BEER_RATING),
                )
                db.commit()
            except db.IntegrityError:
                error = f"'{BEER_NAME}' from '{BREWERY_NAME}' has already been logged by user '{USERNAME}' in the past."
        if error is not None:
            flash(error)
    return render_template("checkin/log_beer.html", brewery_list=brewery_list)