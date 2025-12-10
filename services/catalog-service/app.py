from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ---------------------------------------------------------
# 1. "Catalogue" ultra simple : liste d'articles en mémoire
# ---------------------------------------------------------
PRODUCTS = [
    {"id": 1, "name": "T-shirt DevOps", "price": 19.99},
    {"id": 2, "name": "Mug Terraform", "price": 12.50},
    {"id": 3, "name": "Sticker Kubernetes", "price": 3.00},
]


# ---------------------------------------------------------
# 2. Page d'accueil : redirige vers /products
# ---------------------------------------------------------
@app.route("/")
def home():
    return redirect(url_for("list_products"))


# ---------------------------------------------------------
# 3. Page produits : affiche les articles
#    - lit éventuellement le paramètre ?user= dans l'URL
# ---------------------------------------------------------
@app.route("/products")
def list_products():
    user = request.args.get("user", "invité")

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

    return render_template_string(products_page, user=user, products=PRODUCTS)


if __name__ == "__main__":
    # Pour tes tests en local :
    # - host="0.0.0.0" pour que ce soit accessible depuis Docker
    # - port=5001 pour catalog-service
    app.run(host="0.0.0.0", port=5001, debug=True)
