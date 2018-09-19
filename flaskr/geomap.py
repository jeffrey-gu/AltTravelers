from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('geomap', __name__, url_prefix='/geomap')

@bp.route('/', methods=('GET','POST'))
def mapview():
    return render_template('geomap/mapview.html')
