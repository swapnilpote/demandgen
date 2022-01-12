import logging
from flask import Flask

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

if app.config.get("ENV") == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config.get("ENV") == "testing":
    app.config.from_object("config.TestingConfig")
elif app.config.get("ENV") == "development":
    app.config.from_object("config.DevelopmentConfig")

from app.mod.api.v1.views import blueprint_demandgen

app.register_blueprint(blueprint_demandgen, url_prefix="/api/v1")