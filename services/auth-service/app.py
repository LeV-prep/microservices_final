import os
import psycopg2
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

def check_credentials(username: str, password: str) -> bool:
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT", "5432"))
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not all([host, dbname, user, db_password]):
        raise RuntimeError("Missing DB env vars: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD")

    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=db_password,
        sslmode="require",
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE username=%s AND password=%s LIMIT 1;",
        (username, password),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row is not None


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            ok = check_credentials(username, password)
        except Exception as e:
            # Message clair pour le TP (évite de masquer l'erreur)
            return f"Erreur connexion DB: {e}", 500

        if ok:
            catalog_url = f"http://localhost:5001/products?user={username}"
            return redirect(catalog_url)
        else:
            error_message = "Identifiants incorrects. Réessaie 🙂"

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
    app.run(host="0.0.0.0", port=5000, debug=True)
