from flask import Blueprint

# Vytvoříme instanci Blueprintu s názvem 'main'
bp = Blueprint('main', __name__)

# Na konci naimportujeme naše routy, abychom předešli cyklickým závislostem
from app.main import routes