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
            top_badge = badge[-1]["image"]
        scores.append({'name': name, 'score': points, "badge": top_badge})
    

    sort = sorted(scores, key=lambda item: item['score'], reverse=True)
    sort[0]['badge'] = "no1.png"
    return sort[:3]



def get_user_badge(user):
    badge_db = badges.load_badges()
    user_badge_names = user.get('badges', [])
    full_badges = []
    for name in user_badge_names:
        Badge = tinydb.Query()
        result = badge_db.search(Badge.name == name)
        if result:
            full_badges.append(result[0])  # append full badge object

    print("FULL BADGES RETURNED:", full_badges)
    return full_badges