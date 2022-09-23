import os
import base64
import io
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
import matplotlib.pyplot as plt
plt.switch_backend('Agg')

# DEFINING THE BLUEPRINT CALLED `stats`
bp = Blueprint("stats", __name__, url_prefix="/stats")

# DEFINING THE get_stats VIEW AND REGISTERING IT WITH THE stats BLUEPRINT


@bp.route("/", methods=("GET", "POST"))
@login_required
def get_stats():
    db = get_db()
    last_five_beers_df = pd.read_sql_query(
        f'''
        select
            beer_name as beer,
            brewery_name as brewery,
            beer_type as type,
            date(CHECKIN_DATE) as date,
            beer_rating as rating
        from
            beers
        where
            username = '{g.user['username']}'
        order by datetime(CHECKIN_DATE) desc
        ''', db)

    BEER_TYPES_HIST_IMAGE_NAME = f"{g.user['username']}_beer_types_plot.png"
    generate_beer_type_histogram(
        last_five_beers_df, BEER_TYPES_HIST_IMAGE_NAME)

    BEER_RATINGS_HIST_IMAGE_NAME = f"{g.user['username']}_beer_ratings_plot.png"
    generate_beer_ratings_histogram(
        last_five_beers_df, BEER_RATINGS_HIST_IMAGE_NAME)

    return render_template("stats/get_stats.html", last_five_beers_df=last_five_beers_df.head(5), beer_types_histogram=BEER_TYPES_HIST_IMAGE_NAME, beer_ratings_histogram=BEER_RATINGS_HIST_IMAGE_NAME)


def generate_beer_type_histogram(dataframe, IMAGE_NAME):
    # GENERATE BEER TYPE HISTOGRAM
    try:
        os.remove(IMAGE_NAME)
    except:
        pass
    root_dir = os.path.dirname(os.getcwd())
    IMG_PATH = os.path.join(root_dir, 'BeerMe', 'beerme',
                            'static', f'{IMAGE_NAME}')
    plt.clf()
    plt.hist(dataframe.type, color='#eedb02', bins=20)
    plt.savefig(IMG_PATH)


def generate_beer_ratings_histogram(dataframe, IMAGE_NAME):
    # GENERATE BEER TYPE HISTOGRAM
    try:
        os.remove(IMAGE_NAME)
    except:
        pass
    root_dir = os.path.dirname(os.getcwd())
    IMG_PATH = os.path.join(root_dir, 'BeerMe', 'beerme',
                            'static', f'{IMAGE_NAME}')
    plt.clf()
    plt.hist(dataframe.rating, color='#54b8f9', bins=20)
    plt.savefig(IMG_PATH)
