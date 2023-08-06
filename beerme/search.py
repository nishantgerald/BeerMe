import io
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
from beerme.db import get_db
from beerme.auth import login_required
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Response
plt.switch_backend('Agg')

# DEFINING THE BLUEPRINT CALLED `search`
bp = Blueprint("search", __name__, url_prefix="/search")

# DEFINING THE get_stats VIEW AND REGISTERING IT WITH THE stats BLUEPRINT


@bp.route("/", methods=("GET", "POST"))
@login_required
def get_search_results():
    db = get_db()
    
    if request.method == "POST":
        search_query = request.form["search_term"]
    else:
        search_query = ""
    
    search_results_df = pd.DataFrame()
    
    historical_beers_df = pd.read_sql_query(
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
    if search_query:
        # Filtering the DataFrame based on the search query
        filtered_series = historical_beers_df.apply(lambda x: x.astype(str).str.contains(search_query, case=False)).any(axis=1)
        search_results_df = historical_beers_df[filtered_series]
    
    return render_template("search/search.html", search_results_df=search_results_df)
