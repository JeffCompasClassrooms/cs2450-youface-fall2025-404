import flask, tinydb

from handlers import copy, leaderboard
from db import posts, users, helpers, badges

blueprint = flask.Blueprint("login", __name__)
def award_login_badge(user, users_table):
    login_badge_name = "Login for the first time"
    print(f"[AWARD_BADGE] Checking if user has '{login_badge_name}' badge...")
    if login_badge_name not in user.get('badges', []):
        if 'badges' not in user:
            user['badges'] = []
        user['badges'].append(login_badge_name)
        User = tinydb.Query()
        users_table.update({'badges': user['badges']}, User.username == user['username'])
        print(f"[AWARD_BADGE] Awarded login badge to {user['username']}. Current badges: {user['badges']}")
    else:
        print(f"[AWARD_BADGE] User already has the badge. No changes made.")


@blueprint.route('/loginscreen')
def loginscreen():
    """Present a form to the user to enter their username and password."""
    db = helpers.load_db()

    # First check if already logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is not None and password is not None:
        if users.get_user(db, username, password):
            # If they are logged in, redirect them to the feed page
            flask.flash('You are already logged in.', 'warning')
            return flask.redirect(flask.url_for('login.index'))

    return flask.render_template('login.html', title=copy.title,
            subtitle=copy.subtitle)

@blueprint.route('/login', methods=['POST'])
def login():
    """Log in the user.

    Using the username and password fields on the form, create, delete, or
    log in a user, based on what button they click.
    """
    db = helpers.load_db()
    users_table = db.table('users')  # TinyDB users table


    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    print(f"[LOGIN] Attempting login for user: {username}")


    resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
    resp.set_cookie('username', username)
    resp.set_cookie('password', password)
    user = users.get_user(db, username, password)
    print(f"[LOGIN] Fetched user from DB: {user}")
    if user:
        award_login_badge(user, users_table)


    submit = flask.request.form.get('type')
    if submit == 'Create':
        if users.new_user(db, username, password) is None:
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('Username {} already taken!'.format(username), 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))
        flask.flash('User {} created successfully!'.format(username), 'success')
        print(f"[CREATE] User created: {username}")
        user = users.get_user(db, username, password)
        print(f"[CREATE] Fetching new user for badge check: {user}")
        award_login_badge(user, users_table)

    elif submit == 'Delete':
        if users.delete_user(db, username, password):
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('User {} deleted successfully!'.format(username), 'success')
    user_after = users.get_user(db, username, password)
    print(f"[LOGIN] User badges after login: {user_after.get('badges', [])}")
    return resp

@blueprint.route('/logout', methods=['POST'])
def logout():
    """Log out the user."""
    db = helpers.load_db()

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/')
def index():
    """Serves the main feed page for the user."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username is None or password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    users_table = db.table('users')
    award_login_badge(user, users_table)

    # get the info for the user's feed
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
###Prevent division by zero###
    raw_points = users.get_points(user)
# Make sure points is an integer
    try:
        points = int(raw_points)
    except Exception:
        points = 0

    # Prevent division by zero
    if points < 1:
        points = 1
###Prevent division by zero###
    # sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)
    ldb = leaderboard.get_leaderboard()

    #prevent zero division error
    # calculate top_score to avoid division by zero
    top_score = 1  # default value if empty or top score is zero
    if ldb and ldb[0].get('score', 0) != 0:
        top_score = ldb[0]['score']
    

    #get top badge, if none display default
    print(ldb)

    return flask.render_template('feed.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts=sorted_posts, leaderboard=ldb, points= points,
            top_score = top_score
    )