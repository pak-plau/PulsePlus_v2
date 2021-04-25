from flask import Flask, render_template, request
import urllib, json

f = open("keys/tmdb.txt", "r")
tmdb_link = "https://api.themoviedb.org/3/discover/movie?api_key=" + f.read() + "&with_genres="
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

if(__name__ == "__main__"):
    app.debug = True
    app.run()
