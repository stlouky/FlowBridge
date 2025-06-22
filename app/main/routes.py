from flask import render_template
from app.main import bp

# Toto je hlavní stránka naší aplikace
@bp.route('/')
def index():
    # Použijeme funkci render_template k zobrazení našeho HTML souboru
    return render_template('index.html')