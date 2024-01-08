from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify)
from app.utils import *
from app.db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os

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

@session_bp.route('/profil_recherche', methods=('GET', 'POST'))
def profil_recherche():
    if request.method == 'POST':
        db = get_db()
        nom = request.form.get('nom')
        g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom,)).fetchone()
        print(g.recherche['NomUtilisateur'])

        # Vérifier si la requête a renvoyé un résultat
        if g.recherche is not None:
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    else:
        # Set g.recherche to None or an empty dictionary for GET requests
        g.recherche = None
    return render_template('session/profil_recherche.html')
        

@session_bp.route('/portfolio', methods=('GET', 'POST'))
def portfolio():
    db = get_db 
    return render_template('session/portfolio.html')

@session_bp.route('/shop', methods=('GET', 'POST'))
def shop():
    db = get_db 
    return render_template('session/shop.html')
