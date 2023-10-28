from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, app, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

# Création d'un blueprint contenant les routes ayant le préfixe /home
homes_bp = Blueprint('homes', __name__, url_prefix='/homes')

# Création de la route
@homes_bp.route('/homes', methods=('GET', 'POST'))
def homes():
    # On récupère la base de donnée
    db = get_db 
    # à compléter
    return render_template('/page_accueil.html')
    