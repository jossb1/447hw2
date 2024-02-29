from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from hw2.db import get_db

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    db = get_db()
    users = db.execute(
        'SELECT name, id, points FROM user'
    ).fetchall()
    return render_template('site/index.html', users=users)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('site.index'))

    return render_template('site/create.html')


def get_user(id):
    user = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    return user


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    user = get_user(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('site.index'))

    return render_template('site/update.html', user=user)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_user(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('site.index'))
