#!/bin/bash

# Nom de l'image Docker
IMAGE_NAME="pictsmanager"

# Construction de l'image Docker
docker build -t $IMAGE_NAME .

# Lancement d'un conteneur à partir de l'image Docker
docker run -it -p 8000:8000 $IMAGE_NAME