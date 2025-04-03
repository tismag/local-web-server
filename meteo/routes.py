from flask import Blueprint, render_template
import requests

# Créer un blueprint pour la météo
meteo_bp = Blueprint('meteo', __name__)

LAT, LON = 45.1885, 5.7245  
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Paris&forecast_days=2"

@meteo_bp.route('/')
def index():
    response = requests.get(URL)
    data = response.json()

    if "current_weather" in data:
        weather = {
            "temperature": data["current_weather"]["temperature"],
            "windspeed": data["current_weather"]["windspeed"],
            "weathercode": data["current_weather"]["weathercode"]
        }
    else:
        weather = None

    return render_template('index.html', weather=weather)