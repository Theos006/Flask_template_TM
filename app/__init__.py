import os
from flask import Flask
from app.utils import *

# Importation des blueprints de l'application
# Chaque blueprint contient des routes pour l'application
from app.views.home import home_bp
from app.views.auth import auth_bp
from app.views.user import user_bp
from app.views.page_exemple import test_bp
from app.views.page_accueil import homes_bp
from app.views.connection_ou_creation import connection_ou_creation_bp
from app.views.creation_compte_createur import creation_compte_createur_bp
from app.views.creation_createur_ou_client import creation_createur_ou_client_bp

# Fonction automatiquement appelée par le framework Flask lors de l'exécution de la commande python -m flask run permettant de lancer le projet
# La fonction retourne une instance de l'application créée
def create_app():

    # Crée l'application Flask
    app = Flask(__name__)

    # Chargement des variables de configuration stockées dans le fichier config.py
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), "config.py"))

    # Enreigstrement des blueprints de l'application.
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(homes_bp)
    app.register_blueprint(connection_ou_creation_bp)
    app.register_blueprint(creation_compte_createur_bp)
    app.register_blueprint(creation_createur_ou_client_bp)

    # On retourne l'instance de l'application Flask
    return app
