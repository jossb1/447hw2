from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from hw2.db import get_db

bp = Blueprint('site', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        query = request.form['query']

        if query:
            int_query = None
            try:
                float_query = float(query)
                if float_query.is_integer() and float_query >= 0:
                    int_query = int(float_query)
            except ValueError:
                pass

            db = get_db()
            if int_query is None:
                users = db.execute(
                    'SELECT name, id, points FROM user'
                    " WHERE name LIKE ? OR name LIKE ?"
                    " ORDER BY name", (f"{query}%", f"% {query}%")
                ).fetchall()
            else:
                users = db.execute(
                    'SELECT name, id, points FROM user'
                    " WHERE name LIKE ? OR name LIKE ?"
                    " OR points = ? OR id = ?",
                    (f"{query}%", f"% {query}%", int_query, int_query)
                ).fetchall()
            return render_template('site/index.html', users=users, query=query)

    db = get_db()
    users = db.execute(
        'SELECT name, id, points FROM user'
    ).fetchall()
    return render_template('site/index.html', users=users)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        points = request.form['points']
        error = None

        if not name or not points:
            error = 'Both fields are required.'

        try:
            points = float(points)
            if points.is_integer() and points >= 0:
                points = int(points)
            else:
                error = 'Points must be a non-negative whole number'
        except ValueError:
            error = 'Points must be a non-negative whole number'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO user (name, points)'
                ' VALUES (?, ?)',
                (name, points)
            )
            db.commit()
            return redirect(url_for('site.index'))

    return render_template('site/create.html')


def get_user(id):
    user = get_db().execute(
        'SELECT name, id, points FROM user'
        ' WHERE id = ?', (id,)
    ).fetchone()

    return user


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    user = get_user(id)

    if request.method == 'POST':
        name = request.form['name']
        points = request.form['points']
        error = None

        if not name or not points:
            error = 'Both fields are required.'

        try:
            points = float(points)
            if points.is_integer() and points >= 0:
                points = int(points)
            else:
                error = 'Points must be a non-negative whole number'
        except ValueError:
            error = 'Points must be a non-negative whole number'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET name = ?, points = ?'
                ' WHERE id = ?', (name, points, id)
            )
            db.commit()
            return redirect(url_for('site.index'))

    return render_template('site/update.html', user=user)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('site.index'))
