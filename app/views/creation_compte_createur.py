from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, app)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

# Création d'un blueprint contenant les routes ayant le préfixe...
creation_compte_createur_bp= Blueprint('creation_compte_createur', __name__, url_prefix='/auth')

# Création de la route
@creation_compte_createur_bp.route('/creation_compte_createur', methods=('GET', 'POST'))
def creation_compte_createur():
    # On récupère la base de donnée
    db = get_db 
    # à compléter
    return render_template('/creation_compte_createur.html')
    