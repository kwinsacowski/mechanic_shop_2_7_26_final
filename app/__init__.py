import os
from flask import Flask
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
from app.extensions import db, ma, limiter, cache
from config import TestingConfig, DevelopmentConfig

load_dotenv()

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Mechanic Shop API"
    }
)

CONFIG_MAP = {
    "DevelopmentConfig": DevelopmentConfig,
    "TestingConfig": TestingConfig
}

def create_app(config_name="DevelopmentConfig") -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    if config_name == "TestingConfig":
        app.config.from_object(CONFIG_MAP["TestingConfig"])
    else:
        app.config.from_object(CONFIG_MAP["DevelopmentConfig"])
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    import app.models as models

    from app.blueprints.customers import customers_bp
    from app.blueprints.mechanics import mechanics_bp
    from app.blueprints.service_tickets import service_tickets_bp
    from app.blueprints.inventory import inventory_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    with app.app_context():
        db.create_all()

    @app.get("/")
    def home():
        return {
            "status": "Mechanic Shop API running",
            "swagger_ui": "http://127.0.0.1:5000/api/docs",
            "swagger_yaml": "http://127.0.0.1:5000/static/swagger.yaml",
        }


    return app