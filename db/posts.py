import time
import tinydb
from . import users

def add_post(db, user, text):
    posts = db.table('posts')
    badge = users.get_top_badge(user)
    posts.insert({'user': user['username'], 'text': text, 'time': time.time(), 'badge': badge})

def get_posts(db, user):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.search(Post.user==user['username'])
