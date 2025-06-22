# Tento soubor bude jediný, který budeme přímo spouštět
from app import create_app

# Zavoláme naši "továrnu na aplikace" z app/__init__.py
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)