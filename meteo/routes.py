from flask import render_template
from .import meteo_bp
from datetime import datetime
import requests

LAT, LON = 45.1765, 5.7364

# Récupérer les données hourly (toutes les infos possibles)
URL = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}&"
    f"hourly=temperature_2m,apparent_temperature,precipitation,weathercode,cloudcover,windspeed_10m&"
    f"timezone=Europe/Paris&forecast_days=7"
)

jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

@meteo_bp.route('/')
def index():
    response = requests.get(URL)
    data = response.json()
    hourly = data.get("hourly", {})
    
    # --- Filtrage horaires ---
    filt_heures = [7, 12, 18]  # heures clés pour prochains jours
    hourly_filtered = {k: [] for k in hourly if k != "time"}
    heures_affichees = []
    jours_affiche = []

    now = datetime.now()

    for i, t in enumerate(hourly["time"]):
        dt = datetime.fromisoformat(t)

        # 1️⃣ Heures restantes aujourd’hui
        if dt.date() == now.date() and dt.hour >= now.hour:
            for key in hourly_filtered:
                hourly_filtered[key].append(hourly[key][i])
            heures_affichees.append(dt.strftime("%H:%M"))
            jours_affiche.append(f"Aujourd'hui")

        # 2️⃣ Heures clés pour les prochains jours
        elif dt.hour in filt_heures and dt.date() != now.date():
            for key in hourly_filtered:
                hourly_filtered[key].append(hourly[key][i])
            heures_affichees.append(dt.strftime("%H:%M"))
            jours_affiche.append(f"{jours_fr[dt.weekday()]} {dt.day}/{dt.month}")

    hourly_filtered["heures"] = heures_affichees
    hourly_filtered["jours"] = jours_affiche

    return render_template("meteo/index.html", weather=hourly_filtered)
