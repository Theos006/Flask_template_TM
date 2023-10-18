from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, app)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

# Création d'un blueprint contenant les routes ayant le préfixe...
connection_ou_creation_bp = Blueprint('connection_ou_creation', __name__, url_prefix='/auth')

# Création de la route
@connection_ou_creation_bp.route('/connection_ou_creation', methods=('GET', 'POST'))
def connection_ou_creation():
    # On récupère la base de donnée
    db = get_db 
    # à compléter
    return render_template('/connection_ou_creation.html')