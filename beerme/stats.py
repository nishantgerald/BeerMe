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

# DEFINING THE BLUEPRINT CALLED `stats`
bp = Blueprint("stats", __name__, url_prefix="/stats")

# DEFINING THE get_stats VIEW AND REGISTERING IT WITH THE stats BLUEPRINT


@bp.route("/", methods=("GET", "POST"))
@login_required
def get_stats():
    db = get_db()
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
    plot_beer_types()
    plot_beer_ratings()
    return render_template("stats/get_stats.html", historical_beers_df=historical_beers_df,last_five_beers_df=historical_beers_df.head(5))

@bp.route('/images/beer_types_hist.png')
def plot_beer_types():
    fig, ax = create_blank_figure()
    db = get_db()
    beer_types= pd.read_sql_query(
        f'''
        select
            beer_type as type
        from
            beers
        where
            username = '{g.user['username']}'
        ''', db)
    sns.histplot(beer_types.type, ax=ax, discrete=True,color='#eedb02', alpha=0.75)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title('Distribution of Beer Types', fontsize=18)
    ax.set_xlabel("Type of Beer")
    ax.set_ylabel("Beer Count")
    ax.tick_params(axis='x', rotation=90)
    ax.figure.tight_layout()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@bp.route('/images/beer_ratings_hist.png')
def plot_beer_ratings():
    fig, ax = create_blank_figure()
    db = get_db()
    beer_ratings= pd.read_sql_query(
        f'''
        select
            beer_rating as rating
        from
            beers
        where
            username = '{g.user['username']}'
        ''', db)
    sns.set_style("whitegrid")
    sns.histplot(beer_ratings.rating, ax=ax, binrange=(0,5), bins=20, color='#eedb02', alpha=0.75)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title('Distribution of Beer Ratings', fontsize=18)
    ax.set_xlabel("Beer Rating")
    ax.set_ylabel("Beer Count")
    ax.tick_params(axis='x', rotation=0)
    ax.figure.tight_layout()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_blank_figure():
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    return fig, ax