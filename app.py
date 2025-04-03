#!/usr/bin/python3

from flask import Flask, render_template
import requests

app = Flask(__name__)

from flask import Flask, render_template
import requests

app = Flask(__name__)

# Coordonnées GPS de Grenoble
LAT, LON = 45.1885, 5.7245  
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Paris&forecast_days=2"

@app.route('/')
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

