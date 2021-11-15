from db import get_db

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
        return {'status': 'Please set a value for headrest'}

    if sheet is None:
        return {'status': 'Please mount a sheet'}

    return {
        'data': {
            'headrest': headrest['value'],
            'sheet': {
                'last_changed': sheet['changed_date'],
                'color': sheet['color']
            }
        }
    }