from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('geomap', __name__)
# , url_prefix='/geomap')

@bp.route('/')
@login_required
def mapview():
    # user_id = checkSessionUserId()
    markers = get_db().execute(
        'SELECT lat, lng FROM marker WHERE author_id = ?', (str(g.user['id']),)
    ).fetchall()
    return render_template('geomap/mapview.html', savedMarkers = markers)

# background process
@bp.route('/delete_marker_request', methods=('GET','POST'))
@login_required
def delete_marker_request():
    if request.method == 'POST':
        lat = request.form['lat']
        lng = request.form['lng']
        error = None

        if not lat:
            error = 'delete_marker_request: lat is not valid'
        elif not lng:
            error = 'delete_marker_request: lng is not valid'
        else:
            db = get_db()
            db.execute(
                'DELETE FROM marker'
                ' WHERE author_id = ? and lat = ? and lng = ?',
                (g.user['id'], lat, lng)
            )
            db.commit()
        if error is not None:
            flash(error)
            return redirect(url_for('geomap.mapview'), "FAILURE: marker deletion");
        return redirect(url_for('geomap.mapview'), "SUCCESS: marker deletion");

# background process
@bp.route('/create_marker_request', methods=('GET', 'POST'))
@login_required
def create_marker_request():
    if request.method == 'POST':
        title = request.form['title']
        lat = request.form['lat']
        lng = request.form['lng']
        error = None

        if not lat:
            error = 'create_marker_request: lat is not valid'
        elif not lng:
            error = 'create_marker_request: lng is not valid'
        else:
            db = get_db()
            db.execute(
                'INSERT INTO marker (author_id, title, lat, lng)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], title, lat, lng)
            )
            db.commit()

        if error is not None:
            flash(error)
            return redirect(url_for('geomap.mapview'), "FAILURE: marker creation");
        return redirect(url_for('geomap.mapview'), "SUCCESS: marker creation");
