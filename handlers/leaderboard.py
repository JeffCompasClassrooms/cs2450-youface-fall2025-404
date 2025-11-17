import flask
import tinydb
from db import posts, users, helpers, badges

blueprint = flask.Blueprint('leaderboard',__name__)
@blueprint.route('/leaderboard')
def get_leaderboard():
    scores = []
    db = helpers.load_db()
    users = db.table('users')
    all = users.all()
    for user in all:
        points = user.get('points', 0)
        name = user.get('username', 'Unknown')
        badge = get_user_badge(user)
        if not badge:
            top_badge = "base_duck.png"
        else:
            top_badge = badges.get_badge_png_by_name(badge[-1])
        scores.append({'name': name, 'score': points, "badge": top_badge})
    

    sort = sorted(scores, key=lambda item: item['score'], reverse=True)
    sort[0]['badge'] = "no1.png"
    return sort[:3]



def get_user_badge(user):
    badge_db = badges.load_badges()
    all_badges = user.get('badges', [])
    return all_badges
   