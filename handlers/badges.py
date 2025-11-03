import flask

from db import posts, users, helpers

blueprint = flask.Blueprint('badges',__name__)
@blueprint.route('/badges')
def get_badges():
    badges_list = []
    db = helpers.load_db()
    badges_table = db.table('badges')  # Access the badges table
    all_badges = users.getbadges(badges_table)  # Call your getbadges function from users.py
    for b in all_badges:
        badges_list.append({
            'id': b[0],
            'name': b[1],
            'value': b[2],
            'description': b[3],
            'requirement': b[4],
            'img': b[5]
        })
    
    sorted_badges = sorted(badges_list, key=lambda item: item['value'], reverse=True)
    return flask.render_template('badges.html', title='Badges', badges=sorted_badges)
    
    #return flask.render_template('index.html', title='Leaderboard', leaderboard=leaderboard)