from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from db import get_db

bp = Blueprint('headrest', __name__, url_prefix='/headrest')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def set_headrest():
    if request.method == 'POST':
        angle = request.form['angle']

        if not angle:
            return jsonify({'status': 'Angle is required.'}), 403

        db = get_db()
        db.execute(
            'INSERT INTO headrest (value)'
            ' VALUES (?)',
            (angle,)
        )
        db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM headrest'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Headrest succesfully recorded/retrieved',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'value': check['value']
        }
    }), 200