from flask import (
    Blueprint, request, jsonify
)

from auth import login_required
from db import get_db

bp = Blueprint('sheet', __name__, url_prefix='/sheet')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def set_headrest():
    if request.method == 'POST':
        sheet = request.form['sheet']

        if not sheet:
            return jsonify({'status': 'Sheet is required.'}), 403

        db = get_db()
        db.execute(
            'INSERT INTO sheet (color)'
            ' VALUES (?)',
            (sheet,)
        )
        db.commit()

    check = get_db().execute(
        'SELECT id, changed_date, color'
        ' FROM sheet'
        ' ORDER BY changed_date DESC'
    ).fetchone()
    return jsonify({
        'status': 'Sheet succesfully recorded/retrieved',
        'data': {
            'id': check['id'],
            'changed_date': check['changed_date'],
            'color': check['color']
        }
    }), 200
