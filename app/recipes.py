import json
import requests
import random
import sqlite3

edamam_id = open("keys/edamamid.txt", "r").read()
edamam_key = open("keys/edamamkey.txt", "r").read()

DB_FILE = "data.db"

class DataEntry:
    def __init__(self, file=DB_FILE):
        self.db = sqlite3.connect(file, check_same_thread=False)
        self.cursor = self.db.cursor()

    def execute(self, command, bindings=tuple()):
        return self.cursor.execute(command, bindings)

    def close(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def __del__(self):
        self.close()

# creates search query with query, api id and key
def buildQuery(base, **kwargs):
    query = base
    next = "?"
    for key, value in kwargs.items():
        query += f"{next}{key}={value}"
        next = "&"

    return query

def getRecipes(query):

    # stores adds query, API id, and API key into search url
    search = buildQuery(
        "https://api.edamam.com/search", 
        q=query,
        app_id=edamam_id,
        app_key=edamam_key
    )

    # gets recipes based on filter
    response = requests.request("GET", search)
    if response.status_code != 200:
        return None

    response = response.json()

    hits = response['hits']

    recipes = (hit['recipe'] for hit in hits)

    return [
        {'url':r['url'], 'title':r['label'], 'image':r['image']} 
        for r 
        in recipes
    ]

# creates a table for caching recipe info
def createRecipesTable():
    c = DataEntry()

    c.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            url TEXT PRIMARY KEY, 
            title TEXT, 
            image TEXT
        );
    """)

# adds all recipes for a given query into the database 
def addRecipes(hits):
    for hit in hits:
        addRecipe(hit)

# adds info on a recipe to the database
def addRecipe(recipe):
    c = DataEntry()
    
    command = "INSERT INTO recipes (url, title, image) VALUES (?, ?, ?);"
    c.execute(command, (
        recipe['url'], 
        recipe['title'],
        recipe['image']
    ))

# gets a stored recipe from the database
def getRecipeFromCache(query):
    c = DataEntry()

    command = "SELECT * FROM recipes WHERE title LIKE ?"
    bindings = (f"%{query}%", )

    data = c.execute(command, bindings)
    return data.fetchall()

# gets a random recipe from search query
def getRecipe(query):

    from_cache = getRecipeFromCache(query)
    # print("from cache", from_cache[:3])

    if len(from_cache) != 0:
        # print("Using data from the cache")
        return random.choice(from_cache) 

    else:
        # print("Asking the api")
        recipes = getRecipes(query)
        if len(recipes) == 0:
            return None

        addRecipes(recipes)
        return random.choice(recipes)

if __name__ == "__main__":
    createRecipesTable()

    searches = [
        "chicken",
        "breast",
        "soup",
    ] * 2

    for search in searches:
        recipe = getRecipe(search)

        print('-'*10)
        print(f"{search} has recipe: ")
        print(recipe)
        print('-'*10)

    c = DataEntry()
    c.execute("DROP TABLE recipes")
        addRecipe(r)
    db.commit()
    db.close()
    return r

createRecipesTable()
recipe = getRecipeAPI("chicken")
print(recipe)
