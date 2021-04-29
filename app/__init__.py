from flask import Flask, render_template, request
import urllib, json, nyt

f = open("keys/tmdb.txt", "r")
key = f.read()
restaurant_clicked=""
tmdb_link = "https://api.themoviedb.org/3/discover/movie?api_key=" + key + "&with_genres="
title_link = "https://api.themoviedb.org/3/search/movie?api_key=" + key + "&include_adult=true&query="
f.close()

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def root():
    return render_template("home.html", movies="")

@app.route("/get_movies", methods=["GET", "POST"])
def get_movies():
    movies = request.form.getlist("genre")
    if not movies:
        return render_template("home.html", error_genre="Pick at least one genre!", movies="")
    else:
        temp = tmdb_link
        for i in movies:
            temp += str(i) + ","
        temp = temp[:len(temp) - 1]
        data = json.loads(urllib.request.urlopen(temp).read())
        return render_template("home.html", movies=zip(data["results"], nyt.get_links(data)))
    
@app.route("/find_title", methods=["GET", "POST"])
def find_title():
    title = request.form.get("search")
    if not title:
        return render_template("home.html", error_title="Enter at least one character", movies="")
    temp = title_link + title
    data = json.loads(urllib.request.urlopen(temp.replace(" ", "%20")).read())
    return render_template("home.html", movies=zip(data["results"], nyt.get_links(data)))

@app.route("/find_food", methods=["GET", "POST"])
def find_food():
    search = request.form.get("food-name")
    if not search:
        return render_template("home.html", last_search='', focus='food')
    
    recipe = getRecipe(search)

    return render_template("home.html", recipe=recipe, last_search=search, focus='food')

@app.route("/find_restaurant", methods=["GET", "POST"])
def find_restaurant():
    cuisine = request.form.get("cuisine")
    zipcode = request.form.get("zip")
    info=restaurants.getRestaurantAPI(cuisine,zipcode)
    restaurant_clicked="yes"
    if (info==None):
        return render_template("home.html",
                               error_restaurant="No Restaurants Found",
                               name="",
                               cuisine="",
                               rating="",
                               review="",
                               phone="",
                               link = "",
                               zipcode = "",
                               restaurant_clicked=restaurant_clicked)
    else: 
        return render_template("home.html",
                               error_restaurant="",
                               name=info["name"],
                               cuisine=info["cuisine"],
                               rating=info["rating"],
                               review=info["review"],
                               phone=info["phone"],
                               link = info["link"],
                               zipcode = info["zip"],
                               restaurant_clicked=restaurant_clicked)
    
if(__name__ == "__main__"):
    app.debug = True
    nyt.nyt_init()
    app.run()
