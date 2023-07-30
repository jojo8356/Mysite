from flask import *
import datetime
from model import *
from counter import *
from cryptograph import *
import threading

port = 5000
file_db = "db/database.db"
db = Model(file_db)
year = datetime.datetime.now().year
table_account = "account"

def init_variable(colonne):
    try:
        elmt = db.get_elements_from_colonne(table_account, colonne)
    except:
        elmt = []
    return elmt

# css: {{ url_for(dossier ou il y a le fichier, filename = le nom du fichier)}}
# get a input: request.form.get(name of input)
counter = Counter(file_db)
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404


@app.before_request
def define_ephemere_variable():
    passwords = init_variable("password")
    emails = init_variable("email")
    pseudos = init_variable("pseudo")
    g.year = year
    g.passwords = passwords
    g.emails = emails
    g.pseudos = pseudos
    g.table_account = "account"

@app.route("/")
@app.route("/accueil/")
@app.route("/home/")
def accueil():
    counter.count("data", "count_visitor")
    nb_visit = counter.read("data", "count_visitor")
    return render_template("accueil.html", nb_visit=nb_visit)


@app.route("/etc/")
def autres():
    return render_template("autres.html")

@app.route("/leçon_redstone/<number>/", methods=["POST", "GET"])
def leçon_redstone(number):
    return render_template("leçon_redstone/LR%s.html/" % str(number))

@app.route("/introduction/")
def introduction():
    return render_template("introduction.html")

@app.route("/forum/")
def forum():
    return render_template("forum.html")

@app.route("/inscription/", methods=["GET", "POST"])
def inscription():
    error = False
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        email = request.form["email"]
        password = request.form["password"]
        email = encrypt(email)
        password = encrypt(password)
        if pseudo in g.pseudos or password in g.passwords:
            if password in g.passwords and email in g.emails:
                try:
                    index = g.emails.index(email)
                    if g.passwords[index] == password:
                        error = "Ce compte existe déjà"
                except:
                    pass
            elif pseudo in g.pseudos:
                error = "Ce pseudo existe déjà"
            elif email in g.emails:
                error = "Cette adresse e-mail existe déjà"
            return render_template("inscription.html", error=error)
        liste = [["pseudo", "email", "password","verification"], [pseudo, email, password, "False"]]
        db.add_multiple_element(g.table_account, liste)
        return redirect("/send/email/" + pseudo)
    return render_template("inscription.html")

@app.route("/send/email/<username>")
def email_send(username):
    index = g.pseudos.index(username)
    email = g.emails[index]
    with open("send_email.py", "r") as file:
        code = file.read()

    exec(code)
    return render_template("send_email.html", username=username)


@app.route("/verification/<username>")
def verification(username):
    dictio = db.get_db_in_dictio()
    index = g.pseudos.index(username)
    dictio[g.table_account]["verification"][index] = "True"
    db.re_push_dictio_elements_in_db(dictio)
    return render_template("verification.html", username=username)


@app.route("/connexion/", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        dictio = db.get_db_in_dictio()
        error = False
        email = get_input("email")
        password = get_input("password")
        email, password = encrypt(email), encrypt(password)
        index = g.emails.index(email)
        index_email = index
        try:
            index_email = g.emails.index(email)
            index_password = g.passwords.index(password)
            index_pasword = g.passwords.index(password)
            if index_email != index_password:
                error = "Votre compte n'existe pas"
        except:
            error = "Votre compte n'existe pas"
        if not error:
            if email not in g.emails:
                error = "Votre compte n'existe pas"
            elif password not in g.passwords:
                error = "Votre mot de passe n'existe pas"
            elif dictio[g.table_account]["vérification"][index] != "True":
                error = "Vous n'avez pas cliqué sur le lien dans notre email de confirmation<br> <a href='/send/{g.pseudos[index_email]}'> lien de renvoie d'email de confirmation </a>"
        if error:
            return render_template("connexion.html", error=error)
        else:
            return redirect("/home/")
    return render_template("connexion.html")


app.run(port=port)
