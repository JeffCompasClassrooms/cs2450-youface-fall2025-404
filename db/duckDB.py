import tinydb
from . import users, helpers
from tinydb.operations import increment
def add_duck(db, name, value, code):
    db.insert({"name":name, "value":value, "code": code})

def load_ducks():
   db = tinydb.TinyDB("ducks.json")
   if(len(db)== 0):
        add_duck(db, "Duck1", 100, 12345)#temp, just to have one duck
   
   return db

def found_duck(username, code):
    user_db = helpers.load_db()
    
    users = user_db.table('users')
    User = tinydb.Query()
    user = users.get(User.username == username)
    db = load_ducks()
    Duck = tinydb.Query()
    result = db.search(Duck.code == int(code))
    
    if not result:
        return "Invalid code."
    duck = result[0]
    if duck['name'] not in user['ducks']:
        user['ducks'].append(duck['name'])
        user['points'] += duck['value']
        User = tinydb.Query()
        users.update({'ducks': user['ducks'], 'points': user['points']}, User.username == username)
        return '{} found!'.format(duck['name'])
    return "You have {} already.".format(duck['name'])
         #when duck found make sure to run addbadgetouser() from badges.py to add a badge to the user
