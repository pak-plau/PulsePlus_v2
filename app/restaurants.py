import json
import requests
import random

yelp_key = open("keys/key_api0.txt", "r").read()

def getRestaurant(cuisine, zip):
    # contains api key for authorizing request
    headers = {
        'Authorization': ('Bearer ' + yelp_key).replace('\n', '')
    }

    # contains filters for choosing restaurant
    url_params = {
        'term': cuisine.replace(' ', '+'),
        'location': zip.replace(' ', '+'),
        'limit': 1, # ensures that response only returns one restaurant
        'offset': random.randint(0, 9) # randomizes the restaurant returned
    }

    # gets random restaurant from Yelp Fusion API based on filters
    response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=url_params).json()

    # gets Yelp id of the restaurant
    id = response['businesses'][0]['id']

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
        "link": restaurant['url']
    }

    return info
