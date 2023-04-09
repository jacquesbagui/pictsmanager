# Utilisation d'une image de base Python 3.9
FROM python:3.9

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers de requirements.txt dans le conteneur
COPY requirements.txt .

# Installation des dépendances
RUN pip install -r requirements.txt

# Copie des fichiers du projet dans le conteneur
COPY . .

# Installation de la base de données SQLite
RUN python manage.py migrate

# Exposition du port 8000 pour le serveur Django
EXPOSE 8000

# Lancement du serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]