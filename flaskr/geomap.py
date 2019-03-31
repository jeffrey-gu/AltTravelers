from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

import json

bp = Blueprint('geomap', __name__)
# , url_prefix='/geomap')

@bp.route('/')
@login_required
def mapview():
    # user_id = checkSessionUserId()
    savedMarkers = []
    markerData = get_db().execute(
        'SELECT lat, lng FROM marker WHERE author_id = ?', (str(g.user['id']),)
    ).fetchall()
    # print(type(markers))
    # for marker in markers:
    #     print(type(marker))
    #     print(type(marker[0]))
    for marker in markerData:
        savedMarkers.append(list(marker)) # convert each sqlite3.row instance into a list

    print("You have "+str(len(savedMarkers))+" saved markers")
    return render_template('geomap/mapview.html', savedMarkers = map(json.dumps, savedMarkers))  # serialize each element of the list
    # return render_template('geomap/mapview.html', savedMarkers = jsonify(savedMarkers))
    # return render_template('geomap/mapview.html', savedMarkers = savedMarkers)

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
