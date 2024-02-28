import flask as fl
import flask_session

app = fl.Flask(__name__, template_folder="./templates")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
flask_session.Session(app)

# Variables Globales
#fl.session["gamemode"]

@app.route("/", methods=["GET", "POST"])
def index():
    if fl.request.method == "POST":
        gamemode = fl.request.form.get("LOCAL", "IA")
        fl.session["gamemode"] = gamemode

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
        # Subir el nombre a la base de datos (Primero revisar si existe)
        # Iniciar el juego con el modo de juego seleccionado
        
        return fl.redirect("/game")

    elif fl.request.method == "GET":
        return fl.render_template("1player.html")


@app.route("/2players", methods=["GET", "POST"])
def two_players():

    if fl.request.method == "POST":
        # Subir los nombres a la base de datos (Primero revisar si existe)
        # Iniciar el juego con el modo de juego seleccionado
        return fl.redirect("/game")

    elif fl.request.method == "GET":
        return fl.render_template("2players.html")
        

@app.route("/game")
def game():
    gamemode = fl.session.get("gamemode")
    return fl.render_template("game.html", gamemode=gamemode)

