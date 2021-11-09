from flask import (
    Blueprint, jsonify
)

from auth import login_required
from db import get_db

bp = Blueprint('status', __name__, url_prefix='/status')

@bp.route('/')
@login_required
def get_status():
    headrest = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM headrest'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    sheet = get_db().execute(
        'SELECT id, changed_date, color'
        ' FROM sheet'
        ' ORDER BY changed_date DESC'
    ).fetchone()

    if headrest is None:
        return jsonify({'status': 'Please set a value for headrest'}), 404

    if sheet is None:
        return jsonify({'status': 'Please mount a sheet'}), 404

    return jsonify({
        'data': {
            'headrest': headrest['value'],
            'sheet': {
                'last_changed': sheet['changed_date'],
                'color': sheet['color']
            }
        }
    }), 200
