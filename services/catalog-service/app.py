import os
import psycopg2
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

def fetch_products_from_db():
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT", "5432"))
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([host, dbname, user, password]):
        raise RuntimeError("Missing DB env vars: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD")

    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        sslmode="require",  # important pour RDS (comme ton test psql)
    )
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Convertit en liste de dicts comme avant
    return [{"id": r[0], "name": r[1], "price": float(r[2])} for r in rows]


@app.route("/")
def home():
    return redirect(url_for("list_products"))


@app.route("/products")
def list_products():
    user = request.args.get("user", "invité")

    try:
        products = fetch_products_from_db()
    except Exception as e:
        # En cas d’erreur DB, on affiche un message clair dans la page
        return f"Erreur connexion DB: {e}", 500

    products_page = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Catalogue - Mini E-commerce</title>
    </head>
    <body>
        <h1>Catalogue de produits</h1>
        <p>Bonjour {{ user }} 👋</p>

        <h2>Articles disponibles :</h2>
        <ul>
            {% for product in products %}
                <li>
                    <strong>{{ product.name }}</strong>
                    — {{ product.price }} € (id: {{ product.id }})
                </li>
            {% endfor %}
        </ul>

        <p>
            <a href="http://localhost:5000/login">Se déconnecter / changer d'utilisateur</a>
        </p>
    </body>
    </html>
    """

    return render_template_string(products_page, user=user, products=products)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
