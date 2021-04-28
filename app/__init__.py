from flask import Flask, render_template, request
import urllib, json

f = open("keys/tmdb.txt", "r")
key = f.read()
tmdb_link = "https://api.themoviedb.org/3/discover/movie?api_key=" + key + "&with_genres="
title_link = "https://api.themoviedb.org/3/search/movie?api_key=" + key+"&include_adult=true&query="
f.close()

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def root():
    return render_template("home.html", movies="")

@app.route("/get_movies", methods=["GET", "POST"])
def get_movies():
    movies = request.form.getlist("genre")
    if not movies:
        return render_template("home.html", error="Pick at least one genre!", movies="")
    else:
        temp = tmdb_link
        for i in movies:
            temp += str(i) + ","
        temp = temp[:len(temp) - 1]
        print(temp)
        return render_template("home.html", movies=json.loads(urllib.request.urlopen(temp).read()))
    
@app.route("/find_title", methods=["GET", "POST"])
def find_title():
    title = request.form.get("search").replace(" ","+")
    temp = title_link+title
    return render_template("home.html", movies=json.loads(urllib.request.urlopen(temp).read()))

if(__name__ == "__main__"):
    app.debug = True
    app.run()
