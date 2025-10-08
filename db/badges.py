import tindydb
import badges.txt
#fix cause it doesnt work
def load_db_badges():
    for each in badges.txt:
        badges = badges.txt[each]
        db.insert(badges)
    return tinydb.Tinydb("badges.json")

def appendbadges(db, name, value, description):
    db.insert({"name":name, "value":value, "description":description})

def lockedbadges(db, name, value, description, requirements):


