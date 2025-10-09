import flask

from db import posts, users, helpers

blueprint = flask.Blueprint('leaderboard',__name__)
@blueprint.route('/leaderboard')
def get_leaderboard():
    scores=[
        {'name': 'User1', 'score': 120},
        {'name': 'User2', 'score': 95},
        {'name': 'User3', 'score': 80},
        {'name': 'User4', 'score': 75}
        
    ]
    sort = sorted(scores, key=lambda item: item['score'])
    return sort[:3]
    
    #return flask.render_template('index.html', title='Leaderboard', leaderboard=leaderboard)