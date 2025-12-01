import tinydb
# we'll have badges earned through points, actions, and ducks found

# #### World Variables ####
# userbadgesdb = tinydb.TinyDB("userbadges.json")
# badgesdb = tinydb.TinyDB("badges.json")

# #########################

###### This just loads all the badges we want added to badges.json ########
def appendbadges(db, name, value, description, image):
    db.insert({"name":name, "value":value, "description":description,"image":image})

import tinydb

import tinydb

def load_badges():
    db = tinydb.TinyDB("badges.json")  # this file must be empty or proper TinyDB
    # seed badges
    all_badges_to_seed = [
        {"name": "100 points badge", "value": 100, "description": "Earned 100 pts", "image": "100pts.png"},
        {"name": "Login for the first time", "value": 10, "description": "Earn the login badge by logging in for the first time.", "image": "100pts.png"},
        {"name": "Test Badge", "value": 50, "description": "This is a new badge", "image": "100pts.png"},
        {"name": "250 points", "value": 250, "description": "Earned 250 pts", "image": "100pts.png"}
    ]
    
    existing_names = {b['name'] for b in db.all()}
    for badge in all_badges_to_seed:
        if badge['name'] not in existing_names:
            db.insert(badge)
    return db

def add_badge_to_user(user, users):
    badgedb = load_badges()
    for badge in badgedb:
        val = badge['value']
        if is_point_badge(val):
            if user['points'] >= val and badge['name'] not in user['badges']:
                user['badges'].append(badge['name'])
                User = tinydb.Query()
                users.update({'badges': user['badges']}, User.username == user['username'])
                print(user)
def is_point_badge(value):
    try:
        val = int(value)
        if val < 100:
            return False #is duck count badge
        return True
    except ValueError:
        return False #not an int
def is_duck_count_badge(value):
    try:
        val = int(value)
        if val < 100:
            return True #is duck count badge
        return False
    except ValueError:
        return False #not an int
def get_badge_png_by_name(name):
    db = load_badges()
    Badge = tinydb.Query()
    badge=  db.search(Badge.name == name)
    return badge[0].get('image', 'base_duck.png')


