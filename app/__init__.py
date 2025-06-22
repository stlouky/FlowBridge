from flask import Flask
from config import Config

def create_app(config_class=Config):
    # Vytvoříme instanci aplikace
    app = Flask(__name__)
    # Načteme konfiguraci ze souboru config.py
    app.config.from_object(config_class)

    # Zaregistrujeme náš "Blueprint" z modulu 'main'
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Vrátíme vytvořenou a nakonfigurovanou aplikaci
    return app