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
            date(CHECKIN_DATE) as date
        from
            beers
        where
            username = '{g.user['username']}'
        order by datetime(CHECKIN_DATE) desc
        limit
            5
        '''
        , db)
    return render_template("stats/get_stats.html", last_five_beers_df=last_five_beers_df)
