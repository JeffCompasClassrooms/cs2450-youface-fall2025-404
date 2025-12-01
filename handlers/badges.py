import flask, tinydb
from db import posts, users, helpers, badges
from handlers import leaderboard, copy

blueprint = flask.Blueprint('badges', __name__)

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

    # Get all badges in the system
    all_badges = badges.load_badges().all()

    # Get badges the user has earned
    user_badge_names = user.get('badges', [])

    # Filter unearned badges
    unearned_badges = [b for b in all_badges if b['name'] not in user_badge_names]

    # Get full badge objects for badges user owns
    owned_badges = [b for b in all_badges if b['name'] in user_badge_names]

    return flask.render_template(
        'badges.html',
        title="Your Badges",
        badges=owned_badges,
        all_badges=all_badges,
        unearned_badges=unearned_badges,
        user_badge_names=user_badge_names,
        username=username
    )
