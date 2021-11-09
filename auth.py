import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    db = get_db()

    if not username:
        return jsonify({'status': 'Username is required.'}), 403
    elif not password:
        return jsonify({'status': 'Password is required.'}), 403

    try:
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({'status': f'User {username} is already registered.'}), 403

    return jsonify({'status': 'user registered succesfully'}), 200

@bp.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        return jsonify({'status': 'username not found'}), 403
    elif not check_password_hash(user['password'], password):
        return jsonify({'status': 'password is incorrect'}), 403

    session.clear()
    session['user_id'] = user['id']
    return jsonify({'status': 'user logged in succesfully'}), 200


@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'status': 'user logged out succesfully'}), 200


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'status': 'User is not authenticated'}), 403

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
