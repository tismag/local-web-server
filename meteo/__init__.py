from flask import Blueprint

# Créer un blueprint pour la météo
meteo_bp = Blueprint(
    'meteo', __name__,
    static_folder='static',  # Spécifie le chemin vers le dossier static du blueprint
    template_folder='templates'
)