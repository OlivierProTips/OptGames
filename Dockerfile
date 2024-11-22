# Utiliser une image Python officielle
FROM python:3.11-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Flask
EXPOSE 5000

RUN ls -la /app


# Démarrer l'application Flask en production avec Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
