import sqlite3, urllib, json

f = open("keys/nyt.txt", "r")
nyt_link = "https://api.nytimes.com/svc/movies/v2/reviews/search.json?api-key=" + f.read() + "&query="
f.close()

def nyt_init():
    db = sqlite3.connect("pulseplus.db")
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS reviews (title TEXT PRIMARY KEY, link TEXT NOT NULL)")
    db.commit()
    db.close()

def get_links(data):
    links = []
    db = sqlite3.connect("pulseplus.db")
    c = db.cursor()
    for i in data["results"]:
        release_date = ""
        if "release_date" in i:
            release_date = i["release_date"][:4]
        if review_exist(i["title"] + "(" + release_date + ")"):
            info = list(c.execute("SELECT * FROM reviews WHERE title=?", (i["title"] + "(" + release_date + ")",)))
            links.append(info)
        else:
            u = urllib.request.urlopen(nyt_link + urllib.parse.quote_plus(i["title"]))
            info = json.loads(u.read())
            if info["results"] != None:
                for j in info["results"]:
                    insert_review(j["display_title"] + "(" + j["publication_date"][:4] + ")", j["link"]["url"])
            if not review_exist(i["title"] + "(" + release_date + ")"):
                insert_review(i["title"] + "(" + release_date + ")", "No Review")
            link = list(c.execute("SELECT * FROM reviews WHERE title=?", (i["title"] + "(" + release_date + ")",)))
            links.append(link)
    return links

def review_exist(title):
    db = sqlite3.connect("pulseplus.db")
    c = db.cursor()
    results = c.execute("SELECT COUNT(*) FROM reviews WHERE title=?", (title,)).fetchone()
    return results[0] > 0

def insert_review(title, url):
    db = sqlite3.connect("pulseplus.db")
    c = db.cursor()
    c.execute("INSERT OR IGNORE INTO reviews VALUES (?, ?)", (title, url))
    db.commit()
    db.close()
