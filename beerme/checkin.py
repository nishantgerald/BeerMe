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
import pandas as pd

brewery_df=pd.read_csv('beerme/data/brewery.csv', on_bad_lines='skip')[['name']]
brewery_list = brewery_df.name.to_list()

# DEFINING THE BLUEPRINT CALLED `AUTH`
bp = Blueprint("checkin", __name__, url_prefix="/checkin")

@bp.route("/", methods=("GET", "POST"))
@bp.route("/log_beer", methods=("GET", "POST"))
def log_beer():
    if request.method == "POST":
        CHECKIN_DATE = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        BEER_NAME = request.form["BEER_NAME"].lower()
        BEER_TYPE = request.form["BEER_TYPE"].lower()
        BREWERY_NAME = request.form["BREWERY_NAME"].lower()
        BEER_RATING = request.form["BEER_RATING"]
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
                    "INSERT INTO beers (CHECKIN_DATE, BEER_NAME, BEER_TYPE, BREWERY_NAME, BEER_RATING) VALUES (?, ?, ?, ?, ?)",
                    (CHECKIN_DATE, BEER_NAME, BEER_TYPE, BREWERY_NAME, BEER_RATING),
                )
                db.commit()
            except db.IntegrityError:
                error = f"{BEER_NAME} has already been checked in before."
        if error is not None:
            flash(error)
    return render_template("checkin/log_beer.html", brewery_list=brewery_list)