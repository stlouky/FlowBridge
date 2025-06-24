from flask import Flask
# Předpokládám, že zde máte import pro CORS, pokud jste ho použil
# from flask_cors import CORS

def create_app():
    """
    Application Factory - vytváří a konfiguruje Flask aplikaci.
    """
    app = Flask(__name__)

    # >>> PŘIDEJTE TENTO ŘÁDEK <<<
    # Je nezbytný pro fungování sessions (ukládání dat pro uživatele).
    app.config['SECRET_KEY'] = 'a-very-secret-key-for-development'
    # CORS(app) # Pokud používáte CORS, nechte ho zde

    # Zde registrujete vaše blueprinty (tento kód už tam máte)
    from .main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
