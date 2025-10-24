import flask

from handlers import copy, leaderboard
from db import posts, users, helpers
from flask import flash
blueprint = flask.Blueprint("friends", __name__)

@blueprint.route('/addfriend', methods=['POST'])
def addfriend():
    """Adds a friend to the user's friends list."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is None and password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))

    user = users.get_user(db, username, password)
    if not user:
        flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # add the friend
    name = flask.request.form.get('name')
    msg, category = users.add_user_friend(db, user, name)

    flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/unfriend', methods=['POST'])
def unfriend():
    """Removes a user from the user's friends list."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    name = flask.request.form.get('name')
    msg, category = users.remove_user_friend(db, user, name)

    flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/friend/<fname>')
def view_friend(fname):
    """View the page of a given friend."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    friend = users.get_user_by_name(db, fname)
    all_posts = posts.get_posts(db, friend)[::-1] # reverse order
    

    return flask.render_template('friend.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friend=friend['username'],points = friend['points'],
            friends=users.get_user_friends(db, user), posts=all_posts)
@blueprint.route('/friends')
def friends_page():
    """Serves the main feed page for the user."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    # if username is None and password is None:
    #     return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    # if not user:
    #     flask.flash('Invalid credentials. Please try again.', 'danger')
    #     return flask.redirect(flask.url_for('login.loginscreen'))

    # get the info for the user's feed
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
    # sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)
    ldb = leaderboard.get_leaderboard()
    return flask.render_template('friends.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts=sorted_posts, leaderboard=ldb
    )
