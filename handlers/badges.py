import flask, tinydb

from db import posts, users, helpers, badges
from handlers import leaderboard, copy

blueprint = flask.Blueprint('badges',__name__)
@blueprint.route('/badges')
def get_badges():
    db = helpers.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username is None or password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    else:
        user_badges = leaderboard.get_user_badge(user)

    sorted_badges = sorted(user_badges, key=lambda b: int(b['value']), reverse=True)
    return flask.render_template('badges.html', title=copy.title, badges=sorted_badges, username=username)
