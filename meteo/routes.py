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

# Associations code météo - description
WEATHER_DESCRIPTIONS = {
    0: "Ciel dégagé",
    1: "Principalement dégagé",
    2: "Partiellement nuageux",
    3: "Couvert",

    45: "Brouillard",
    48: "Brouillard givrant",

    51: "Bruine légère",
    53: "Bruine modérée",
    55: "Bruine dense",

    56: "Bruine verglaçante légère",
    57: "Bruine verglaçante dense",

    61: "Pluie faible",
    63: "Pluie modérée",
    65: "Pluie forte",

    66: "Pluie verglaçante légère",
    67: "Pluie verglaçante forte",

    71: "Neige faible",
    73: "Neige modérée",
    75: "Neige forte",
    77: "Grains de neige",

    80: "Averses faibles",
    81: "Averses modérées",
    82: "Averses violentes",

    85: "Averses de neige faibles",
    86: "Averses de neige fortes",

    95: "Orage",
    96: "Orage avec grêle légère",
    99: "Orage avec grêle forte",
}


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

    weather_desc = []

    for code in hourly_filtered["weathercode"]:
        weather_desc.append(
            WEATHER_DESCRIPTIONS.get(code, "Conditions météo inconnues")
        )

    hourly_filtered["description"] = weather_desc


    return render_template("meteo/index.html", weather=hourly_filtered)
