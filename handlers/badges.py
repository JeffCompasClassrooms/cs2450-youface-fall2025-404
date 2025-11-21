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
        bdg_db = badges.load_badges()
        Badge = tinydb.Query()
        allbdgs =[]
        not_earned = bdg_db.all()
        for badge in user_badges:
            not_earned = [b for b in not_earned if b["name"] != badge]
            allbdgs.append(bdg_db.search(Badge.name == badge))

    return flask.render_template('badges.html', title=copy.title, badges=allbdgs, username=username, user_badges = user_badges,not_earned = not_earned, subtitle=copy.subtitle, user=user)
def get_all_badges(user):
    user_badges = leaderboard.get_user_badge(user)
    bdg_db = badges.load_badges()
    Badge = tinydb.Query()
    allbdgs =[]
    for badge in user_badges:
        allbdgs.append(bdg_db.search(Badge.name == badge))
    return allbdgs