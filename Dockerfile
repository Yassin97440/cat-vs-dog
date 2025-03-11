# Utiliser une image de base Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et installer les packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port sur lequel FastAPI s'exécutera
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8000"]