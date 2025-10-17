import flask

from db import posts, users, helpers, duckDB

blueprint = flask.Blueprint("posts", __name__)

@blueprint.route('/post', methods=['POST'])
def post():
    """Creates a new post."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    post = flask.request.form.get('post')
    posts.add_post(db, user, post)

    return flask.redirect(flask.url_for('login.index'))
@blueprint.route('/enter', methods=['POST'])
def code_entered():
    code = flask.request.form.get('code')
    username = flask.request.cookies.get('username')
    msg = duckDB.found_duck(username, code)
    flask.flash(msg.format(username))
    return flask.redirect(flask.url_for('login.index'))
    

