# Image de base Python légère
FROM python:3.12-slim

# Créer un dossier de travail dans le conteneur
WORKDIR /app

# Copier les dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .

# Le service écoutera sur le port 5000 à l'intérieur du conteneur
EXPOSE 5000

# Commande de lancement
CMD ["python", "app.py"]
