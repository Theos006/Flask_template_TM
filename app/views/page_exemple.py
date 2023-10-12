from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, app)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os

# Création d'un blueprint contenant les routes ayant le préfixe...
test_bp = Blueprint('test', __name__, url_prefix='/test')


# Création de la route
@test_bp.route('/test', methods=('GET', 'POST'))
def test():
    # On récupère la base de donnée
    db = get_db 
    # à compléter
    return render_template('/pages.html')
    