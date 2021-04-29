import json
import requests
import random
import sqlite3

yelp_key = open("keys/yelp.txt", "r").read()
DB_FILE = "pulseplus.db"
testing = True

# gets information on a restaurant from the Yelp API
# zip MUST be a five digit number
def getRestaurantAPI(cuisine, zip):
    # contains api key for authorizing request
    headers = {
        'Authorization': ('Bearer ' + yelp_key).replace('\n', '')
    }

    # contains filters for choosing restaurant
    url_params = {
        'term': cuisine.replace(' ', '+'),
        'location': zip.replace(' ', '+'),
    }

    # gets list of restaurants from Yelp Fusion API based on filters
    response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=url_params).json()
    businesses = response['businesses']

    # returns None if no businesses have been found
    if (not businesses):
        return None

    # gets Yelp id of a random restaurant
    rand = random.randint(0, len(businesses) - 1)
    id = response['businesses'][rand]['id']

    # gets detailed info about restaurant from Yelp API
    restaurant = requests.get('https://api.yelp.com/v3/businesses/' + id, headers=headers).json()

    # gets reviews on restaurant from Yelp API
    review = requests.get('https://api.yelp.com/v3/businesses/' + id + '/reviews', headers=headers).json()

    # puts together necessary info from requests into a dictionary
    info = {
        'name': restaurant['name'],
        'cuisine': cuisine,
        'rating': restaurant['rating'],
        'review': review['reviews'][0]['text'],
        'phone': restaurant['phone'],
        "link": restaurant['url'],
        "zip": zip
    }

    return info

# creates a table for caching restaurant info
def createRestaurantTable():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS restaurants (name TEXT, cuisine TEXT, rating TEXT,
              review TEXT, phone INT, link TEXT, zip INT);""")
    db.commit()
    db.close()

# adds info on a restaurant to the database
def addRestaurant(info):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO restaurants VALUES (?,?,?,?,?,?,?);"
    c.execute(command, (info['name'], info['cuisine'], info['rating'], info['review'], info['phone'], info['link'], info['zip']))
    db.commit()
    db.close()

# allows sqlite to return info as dictionaries
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# returns info on a restaurant from either the API or the database
def getRestaurant(cuisine, zip):
    db = sqlite3.connect(DB_FILE)
    db.row_factory = dict_factory
    c = db.cursor()

    # gets a restaurant matching the filters from the database
    command = "SELECT * FROM restaurants WHERE cuisine=? AND zip=?;"
    r = c.execute(command, (cuisine, str(zip))).fetchone()
    db.commit()
    db.close()

    # if such restaurant doesn't exist, gets one from the API and adds it to the database
    if (not r or not testing):
        r = getRestaurantAPI(cuisine, zip)
        if (r == None):
            return None
        addRestaurant(r)
    return r;

createRestaurantTable();
restaurant = getRestaurant("pizza", "11214");
print(restaurant)
