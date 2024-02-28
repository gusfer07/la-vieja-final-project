import flask as fl
import flask_session
from cs50 import SQL

app = fl.Flask(__name__, template_folder="./templates")

db = SQL("sqlite:///lavieja.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
flask_session.Session(app)

# Variables Globales


@app.route("/", methods=["GET", "POST"])
def index():
    if fl.request.method == "POST":
        gamemode = fl.request.form.get("LOCAL", "IA")

        if gamemode == "LOCAL":
            return fl.redirect("/2players")
        
        elif gamemode == "IA":
            return fl.redirect("/1player")

        else:
            return fl.render_template("index.html")

    elif fl.request.method == "GET":
        return fl.render_template("index.html")
    

@app.route("/1player", methods=["GET", "POST"])
def one_player():

    if fl.request.method == "POST":
        player1 = fl.request.form.get("player1").strip().capitalize()
        fl.session["player1"] = player1

        if not player1:
            return fl.redirect("/error")

        if not db.execute("SELECT username FROM users WHERE username = ?;", player1):
            db.execute("INSERT INTO users (username) VALUES (?);", player1)
        
        return fl.redirect("/gameIA")

    elif fl.request.method == "GET":
        return fl.render_template("1player.html")


@app.route("/2players", methods=["GET", "POST"])
def two_players():

    if fl.request.method == "POST":

        player1 = fl.request.form.get("player1").strip().capitalize()
        player2 = fl.request.form.get("player2").strip().capitalize()

        if not player1 or not player2:
            return fl.redirect("/error")
        
        elif player1 == player2:
            return fl.redirect("/error")

        fl.session["player1"] = player1
        fl.session["player2"] = player2

        if not db.execute("SELECT username FROM users WHERE username = ?;", player1):
            db.execute("INSERT INTO users (username) VALUES (?);", player1)

        elif not db.execute("SELECT username FROM users WHERE username = ?;", player2):
            db.execute("INSERT INTO users (username) VALUES (?);", player2)

        return fl.redirect("/gameLOCAL")

    elif fl.request.method == "GET":
        return fl.render_template("2players.html")
        

@app.route("/gameIA")
def gameIA():
    player1 = fl.session.get("player1")

    return fl.render_template("gameIA.html", player1=player1)

@app.route("/gameLOCAL")
def gameLOCAL():
    player1 = fl.session.get("player1")
    player2 = fl.session.get("player2")
    
    return fl.render_template("gameLOCAL.html", player1=player1, player2=player2)

@app.route("/error")
def error():
    return fl.render_template("error.html")