import tinydb
# import badges.txt
#fix cause it doesnt work

###### This just loads all the badges we want added to badges.json ########
def appendbadges(db, name, value, description, requirement):
    db.insert({"name":name, "value":value, "description":description, "requirement":requirement})

def load_db_badges(): # this needs to run first before anything else is ever done.
    db = tinydb.TinyDB("badges.json") # maybe make this a world variable instead of local
    db.truncate() # this wipes the json file, which is needed since it stores data even after the run ends
    with open("/root/cs2450-youface-fall2025-404/db/badges.txt","r") as badges:
        for line in badges:
            infolist = line.strip().split(", ")
            name = infolist[0]
            value = infolist[1]
            description = infolist[2]
            requirement = infolist[3]
            if len(infolist) < 4:
                continue
            appendbadges(db, name, value, description, requirement)
    content = db.all()
    print(content) # this just shows whats in badges.json
##########################################################################

def loadbadges(db, name, value, description, requirements):
    pass


load_db_badges()