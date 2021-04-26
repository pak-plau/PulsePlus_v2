import json
import requests
import random

edamam_id = open("keys/edamamid.txt", "r").read()
edamam_key = open("keys/edamamkey.txt", "r").read()

def getRecipe(query):

    # stores adds query, API id, and API key into search url
    search = "https://api.edamam.com/search?q=" + query + "&app_id=$" + edamam_id + "&app_key=$" + edamam_key

    # gets recipes based on filter
    response = requests.get(search).json()

    # generates a random number based on number of recipe results
    rand = random.randint(0, response['count'])

    # gets a random recipe from results
    recipe = response['hits'][rand]['recipe']

    # stores recipe title and image
    title = recipe['label']
    image = recipe['image']

    # puts together necessary info from requests into a dictionary
    info = {
        'recipe title': title,
        'recipe image': image
    }

    return info
