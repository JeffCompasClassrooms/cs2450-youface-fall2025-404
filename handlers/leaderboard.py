import flask

from db import posts, users, helpers

blueprint = flask.Blueprint('leaderboard',__name__)
@blueprint.route('/leaderboard')
def get_leaderboard():
    scores=[
        {'name': 'User1', 'score': 120, 'bar':int(120/120*100)},
        {'name': 'User2', 'score': 95, 'bar':int(95/120*100)},
        {'name': 'User3', 'score': 80, 'bar':int(80/120*100)},
        {'name': 'User4', 'score': 75, 'bar':int(75/120*100)}
        
    ]
    sort = sorted(scores, key=lambda item: item['score'], reverse=True)
    return sort[:3]
    
    #return flask.render_template('index.html', title='Leaderboard', leaderboard=leaderboard)