from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, app)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

# Création d'un blueprint contenant les routes ayant le préfixe...
creation_createur_ou_client_bp = Blueprint('creation_createur_ou_client', __name__, url_prefix='/auth')

# Création de la route
@creation_createur_ou_client_bp.route('/creation_createur_ou_client', methods=('GET', 'POST'))
def creation_createur_ou_client():
    # On récupère la base de donnée
    db = get_db 
    # à compléter
    return render_template('/creation_createur_ou_client.html')
    