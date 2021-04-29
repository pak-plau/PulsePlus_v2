import json
import requests
import random
import sqlite3

edamam_id = open("keys/edamamid.txt", "r").read()
edamam_key = open("keys/edamamkey.txt", "r").read()

DB_FILE = "data.db"

def getRecipeAPI(query):

    # stores adds query, API id, and API key into search url
    search = "https://api.edamam.com/search?q=" + query + "&app_id=$" + edamam_id + "&app_key=$" + edamam_key

    # gets recipes based on filter
    response = requests.request("GET", search)

    # returns None if there are no recipes based on the query
    if (rand < 1):
        return None

    # gets a random recipe from results
    recipe = response['hits'][random.randint(0,20)]['recipe']

    # stores recipe's identifier, title, url, and image
    uri = recipe['uri']
    title = recipe['label']
    url = recipe['url']
    image = recipe['image']

    # puts together necessary info from requests into a dictionary
    info = {
        'recipe identifier': uri,
        'recipe title': title,
        'recipe url': url,
        'recipe image': image
    }

    return info

# creates a table for caching recipe info
def createRecipesTable():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS recipes (identifier TEXT PRIMARY KEY, query TEXT, title TEXT, url TEXT, image TEXT);""")
    db.commit()
    db.close()

# adds info on a recipe to the database
def addRecipe(info):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO recipes VALUES (?, ?, ?, ?, ?);"
    c.execute(command, (info['uri'], info['query'], info['title'], info['url'], info['image']))
    db.commit()
    db.close()

# allows sqlite to return info as dictionaries
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# returns info on a recipe from either the API or the database
def getRecipe(query):
    db = sqlite3.connect(DB_FILE)
    db.row_factory = dict_factory
    c = db.cursor()

    # gets a restaurant matching the query from the database
    command = "SELECT * FROM recipes WHERE query=?;"
    r = c.execute(command, (query)).fetchone()

    # if such a recipe doesn't exist, gets one from the API and adds it to the database
    if (not r):
        r = getRecipeAPI(query)
        if (r == None):
            return None
        addRecipe(r)
    db.commit()
    db.close()
    return r

# createRecipesTable()
# recipe = getRecipeAPI("chicken")
# print(recipe)
