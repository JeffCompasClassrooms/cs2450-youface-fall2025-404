import tinydb
from . import users, helpers, badges
def add_duck(db, name, value, code):
    db.insert({"name":name, "value":value, "code": code})

def load_ducks():
   db = tinydb.TinyDB("ducks.json")
   return db

def found_duck(username, code):
    if(code == ''):
        return "Invalid code.",'none', users.get(User.username == username)
    user_db = helpers.load_db()
    bdg = badges.load_badges()
    print(bdg.all())
    users = user_db.table('users')
    User = tinydb.Query()
    user = users.get(User.username == username)
    db = load_ducks()
    Duck = tinydb.Query()
    result = db.search(Duck.code == int(code))

    if not result:
        return "Invalid code.",'none', users.get(User.username == username)
    duck = result[0]
    if duck['name'] not in user['ducks']:
        user['ducks'].append(duck['name'])
        user['points'] += duck['value']
        User = tinydb.Query()
        users.update({'ducks': user['ducks'], 'points': user['points']}, User.username == username)
        # bdb = badges.load_db_badges()

        return '{} found!'.format(duck['name']), duck['name'], users.get(User.username == username)
    return "You have {} already.".format(duck['name']), duck['name'], users.get(User.username == username)
         #when duck found make sure to run addbadgetouser() from badges.py to add a badge to the user
