import tinydb
import users, helpers

def add_duck(db, name, value, code):
    db.insert({"name":name, "value":value, "code": code})

def load_ducks():
   db = tinydb.Tinydb("badges.json")
   if("badges.json" == ""):
        add_duck(db, "Duck1", 100, 12345)#temp, just to have one duck
   return db

def found_duck(username, code):
    user = users.get_user_by_name(helpers.load_db, username)
    db = load_ducks()
    ducks = db.Query()
    duck = db.search(ducks.code == code)
    if duck.name not in user['ducks']:
        user.ducks.append(duck.code)
        users.points = user.points + duck.value
         #when duck found make sure to run addbadgetouser() from badges.py to add a badge to the user
