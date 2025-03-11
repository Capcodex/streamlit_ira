# Utiliser une image officielle Python comme image de base
FROM python:3.8-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de ton projet dans l'image Docker
COPY . /app

# Installer les dépendances Python depuis requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port que Streamlit utilise
EXPOSE 8501

# Commande pour démarrer l'application Streamlit
CMD ["streamlit", "run", "app.py"]
