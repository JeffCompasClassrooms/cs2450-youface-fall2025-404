import tinydb
# we'll have badges earned through points, actions, and ducks found

# #### World Variables ####
# userbadgesdb = tinydb.TinyDB("userbadges.json")
# badgesdb = tinydb.TinyDB("badges.json")

# #########################

###### This just loads all the badges we want added to badges.json ########
def appendbadges(db, name, value, description, image):
    db.insert({"name":name, "value":value, "description":description,"image":image})

def load_badges():
    db = tinydb.TinyDB("badges.json")
    
    if len(db) <= 0:
        appendbadges(db, "100 points badge", 100, "Earned 100 pts", "100pts.png")
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

    
# def load_db_badges(): # this needs to run first before anything else is ever done.
#     badgesdb.truncate() # this wipes the json file, which is needed since it stores data even after the run ends
#     with open("/root/cs2450-youface-fall2025-404/db/badges.txt","r") as badges:
#         for line in badges:
#             infolist = line.strip().split(", ")
#             id = infolist[0]
#             name = infolist[1]
#             value = infolist[2]
#             description = infolist[3]
#             requirement = infolist[4]
#             image = infolist[5]
#             if len(infolist) < 6:
#                 continue
#             appendbadges(badgesdb, id, name, value, description, requirement, image)
    #content = db.all()
    #print(content) # this just shows whats in badges.json
##########################################################################

# def addbadgetouser(id):
#     badgesdb = load_badges()
#     #userbadgesdb.truncate() # remove after testing, otherwise would wipe badges collected every time ran
#     badgeQ = tinydb.Query()
#     badge = badgesdb.search(badgeQ.id == id) # locates badge based off of id, returns list with badge(dictionary)
#     if badge: # if b has something in  it (True) it means it's a real badge, if so check if it user already has it
#         duplicate = userbadgesdb.search(tinydb.Query().id == id) # this sets duplicate to a badge, if the badge were trying to find is already in the user badges
#         if duplicate: # if duplicate has something, don't add
#             print("duplicate badge attempted to be added, rejected badge")
#         else: # if duplicate is empty, it means the id was not found in userbadges so add this since it's a new badge
#             id, name, value, description, requirement, image = badge[0].values() # badge is a list of a dictionary, so get first item and values only
#             appendbadges(userbadgesdb, id, name, value, description, requirement, image)
#             print(userbadgesdb.all())
#     else: 
#         print(f"badge not found in badges.txt")


# load_db_badges()
# userbadgesdb.truncate()
# addbadgetouser('01')
