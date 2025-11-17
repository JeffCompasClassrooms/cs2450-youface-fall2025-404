import time
import tinydb
from . import users
from handlers import leaderboard

def add_post(db, user, text):
    posts = db.table('posts')
    badge = users.get_top_badge(user)
    ldb = leaderboard.get_leaderboard()
    if(user['username'] == ldb[0]['name']):
        badge = 'no1.png'
    posts.insert({'user': user['username'], 'text': text, 'time': time.time(), 'badge': badge})

def get_posts(db, user):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.search(Post.user==user['username'])
