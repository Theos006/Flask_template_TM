from flask import (Blueprint, render_template)
from app import login_required
from app.utils import *
from app.db.db import get_db
from flask import request

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/accueil_connecte', methods=('GET', 'POST'))
@login_required
def accueil_connecte():
    list_nom = [1, 2, 3, 4]
 
    if request.method == 'POST':
        db = get_db()
        recherche = request.form['recherche']
        # création d'une liste stockant les 10 id utilisateur dont le nom ressemble le plus à la recherche
        result = db.execute("SELECT NomUtilisateur FROM Utilisateur WHERE NomUtilisateur LIKE ? LIMIT 10", ('%' + recherche + '%',))
        list_nom = [row[0] for row in result.fetchall()]

    print(list_nom)

    return render_template('session/accueil_connecte.html', list_nom=list_nom)

@session_bp.route('/profil', methods=('GET', 'POST'))
def profil():
    db = get_db 
    return render_template('/profil.html')

@session_bp.route('/portfolio', methods=('GET', 'POST'))
def portfolio():
    db = get_db 
    return render_template('/portfolio.html')

@session_bp.route('/shop', methods=('GET', 'POST'))
def shop():
    db = get_db 
    return render_template('/shop.html')
