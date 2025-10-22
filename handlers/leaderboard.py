import flask

from db import posts, users, helpers

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
        scores.append({'name': name, 'score': points})
    
    sort = sorted(scores, key=lambda item: item['score'], reverse=True)
    return sort[:3]
    
    #return flask.render_template('index.html', title='Leaderboard', leaderboard=leaderboard)