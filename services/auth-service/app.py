from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ---------------------------------------------------------
# 1. "Base de données" ultra simple : un seul utilisateur
# ---------------------------------------------------------
VALID_USERNAME = "victor"
VALID_PASSWORD = "victor"  # à NE PAS faire en prod, évidemment


# ---------------------------------------------------------
# 2. Page d'accueil : on redirige vers /login
# ---------------------------------------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------------------------------------------------
# 3. Page de login (GET + POST)
#    - GET : affiche le formulaire
#    - POST : vérifie les identifiants
# ---------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None

    if request.method == "POST":
        # Récupérer les données du formulaire
        username = request.form.get("username")
        password = request.form.get("password")

        # Vérification très basique des identifiants
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            # En vrai on utiliserait un token / cookie de session
            # Ici, on fait simple : on passe le nom dans l'URL
            catalog_url = f"http://localhost:5001/products?user={username}"
            return redirect(catalog_url)
        else:
            error_message = "Identifiants incorrects. Réessaie 🙂"

    # Template HTML très simple, inline pour le TP
    login_page = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Connexion - Mini E-commerce</title>
    </head>
    <body>
        <h1>Connexion</h1>

        {% if error_message %}
            <p style="color: red;">{{ error_message }}</p>
        {% endif %}

        <form method="post" action="/login">
            <label for="username">Nom d'utilisateur :</label><br>
            <input type="text" id="username" name="username" required><br><br>

            <label for="password">Mot de passe :</label><br>
            <input type="password" id="password" name="password" required><br><br>

            <button type="submit">Se connecter</button>
        </form>
    </body>
    </html>
    """

    return render_template_string(login_page, error_message=error_message)


if __name__ == "__main__":
    # Pour tes tests en local :
    # - host="0.0.0.0" pour qu'en Docker ce soit accessible
    # - port=5000 pour auth-service
    app.run(host="0.0.0.0", port=5000, debug=True)
