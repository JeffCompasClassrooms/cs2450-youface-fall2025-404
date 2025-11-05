import flask, tinydb

from db import posts, users, helpers

blueprint = flask.Blueprint('badges',__name__)
@blueprint.route('/badges')
def get_badges():
    db = helpers.load_db()
    username = flask.session.get('username')
    userbadges_db = tinydb.TinyDB("userbadges.json")
    user_table = userbadges_db.table(username)
    user_badges = user_table.all()

    if not user_badges:
        user_badges = []  # fallback if none earned yet

    
    sorted_badges = sorted(user_badges, key=lambda b: int(b['value']), reverse=True)
    return flask.render_template('badges.html', title=f"{username}'s Badges", badges=sorted_badges)
