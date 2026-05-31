from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .api.animals import bp as animals_bp
    from .api.search  import bp as search_bp
    from .api.export  import bp as export_bp

    app.register_blueprint(animals_bp, url_prefix="/api/animals")
    app.register_blueprint(search_bp,  url_prefix="/api/search")
    app.register_blueprint(export_bp,  url_prefix="/api/export")

    return app