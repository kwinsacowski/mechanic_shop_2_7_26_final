from flask import Flask
from app.extensions import db, ma, limiter, cache
from config import DevelopmentConfig

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass



def create_app(config_class=DevelopmentConfig) -> Flask:
    flask_app = Flask(__name__, static_folder="static", static_url_path="/static")

    flask_app.config.from_object(config_class)

    # Extensions
    db.init_app(flask_app)
    ma.init_app(flask_app)
    limiter.init_app(flask_app)
    if cache is not None:
        cache.init_app(flask_app)

    # Ensure models are registered before create_all
    import app.models  # noqa: F401

    # Blueprints
    from app.blueprints.customers import customers_bp
    from app.blueprints.mechanics import mechanics_bp
    from app.blueprints.service_tickets import service_tickets_bp
    from app.blueprints.inventory import inventory_bp

    flask_app.register_blueprint(customers_bp, url_prefix="/customers")
    flask_app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    flask_app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
    flask_app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # Swagger UI (optional)
    try:
        from flask_swagger_ui import get_swaggerui_blueprint

        SWAGGER_URL = "/api/docs"
        API_URL = "/static/swagger.yaml"

        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={"app_name": "Mechanic Shop API"},
        )
        flask_app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    except ModuleNotFoundError:
        pass

    with flask_app.app_context():
        db.create_all()

    @flask_app.get("/")
    def home():
        return {
            "status": "Mechanic Shop API running",
            "docs": "/api/docs",
            "swagger_yaml": "/static/swagger.yaml",
        }

    return flask_app
