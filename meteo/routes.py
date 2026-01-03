from flask import render_template
from .import meteo_bp
from datetime import datetime
import requests

LAT, LON = 45.1765, 5.7364

# URL Open-Meteo pour daily et hourly forecast (2 jours)
URL = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}&"
    f"daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,"
    f"precipitation_sum,weathercode,sunrise,sunset,windspeed_10m_max&"
    f"hourly=temperature_2m,apparent_temperature,precipitation,weathercode,cloudcover,windspeed_10m&"
    f"timezone=Europe/Paris&forecast_days=7"
)

# Mapper les jours de la semaine en français
jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

@meteo_bp.route('/')
def index():
    response = requests.get(URL)
    data = response.json()

    # Séparer daily et hourly si présents
    daily = data.get("daily", {})
    hourly = data.get("hourly", {})

    # Current weather si disponible
    current = data.get("current_weather", None)

    # Convertir les dates daily en français
    if daily.get("time"):
        daily["jours"] = []
        for t in daily["time"]:
            dt = datetime.fromisoformat(t)
            day_name = jours_fr[dt.weekday()]
            daily["jours"].append(f"{day_name} {dt.day}/{dt.month}")

    if hourly.get("time"):
        filt_heures = [0, 6, 12, 18]  # heures à garder
        hourly_filtered = {k: [] for k in hourly if k != "time"}  # exclure "time"
        heures = []  # pour afficher dans le template

        for i, t in enumerate(hourly["time"]):
            dt = datetime.fromisoformat(t)
            if dt.hour in filt_heures:
                for key in hourly_filtered:
                    hourly_filtered[key].append(hourly[key][i])
                heures.append(dt.strftime("%H:%M"))

        # remplacer hourly par la version filtrée et ajouter "heures" pour le template
        hourly = hourly_filtered
        hourly["heures"] = heures


    # Construire un dict facile à utiliser dans le template
    weather = {
        "current": current,
        "daily": daily,
        "hourly": hourly
    }

    return render_template('index.html', weather=weather)