import tinydb
# import badges.txt
#fix cause it doesnt work
def appendbadges(db, name, value, description):
    db.insert({"name":name, "value":value, "description":description})
def load_db_badges():
    # for each in badges.txt:
    #     badges = badges.txt[each]
    #     db.insert(badges)
   db = tinydb.Tinydb("badges.json")
   appendbadges(db, "100pts", 100, "Earned your first 100 points!")
   return db



def lockedbadges(db, name, value, description, requirements):
    pass

