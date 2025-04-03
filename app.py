#!/usr/bin/python3

from flask import Flask
from meteo.routes import meteo_bp
from cours_sql.routes import cours_sql_bp

app = Flask(__name__)

app.register_blueprint(meteo_bp, url_prefix='/meteo')
app.register_blueprint(cours_sql_bp, url_prefix='/cours')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

