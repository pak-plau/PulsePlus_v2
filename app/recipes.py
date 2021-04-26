import json
import requests
import random

edamam_key = open("keys/edamam.txt", "r").read()

def getRecipe(query):
    # contains api key for authorizing request
    headers = {
        'Authorization': ('Bearer ' + edamam_key).replace('\n', '')
    }

    # contains filter for narrowing recipes
    url_params = {
        'q': query.replace(' ', '+')
    }

    # gets recipes based on filter
    response = requests.get('https://api.edamam.com/search', headers=headers, params=url_params).json()

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
