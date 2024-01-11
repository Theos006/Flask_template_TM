from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify
)
from app.utils import *
from app.db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/accueil_connecte', methods=('GET', 'POST'))
@login_required
def accueil_connecte():
    list_nom = ["Admin", "Mirko", "Mathieu"]
    list_pdp = []  
    list_bio= []
    db = get_db()
    
    if request.method == 'POST':
        
        recherche = request.form['recherche']
        # création d'une liste stockant les 10 id utilisateur dont le nom ressemble le plus à la recherche
        result = db.execute(
            "SELECT NomUtilisateur FROM Utilisateur WHERE NomUtilisateur LIKE ? LIMIT 10",
            ('%' + recherche + '%',)
        )
        list_nom = [row[0] for row in result.fetchall()]
        
    for nom in list_nom:
        image = db.execute("SELECT PhotoDeProfil FROM Utilisateur WHERE NomUtilisateur = ?", (nom,))
        list_pdp.append(image.fetchone()[0])  
        bio = db.execute("SELECT Biographie FROM Utilisateur WHERE NomUtilisateur = ?", (nom,))
        list_bio.append(bio.fetchone()[0])  

    print(list_nom)
    print(list_bio)
    return render_template('session/accueil_connecte.html', list_nom=list_nom, list_pdp=list_pdp, list_bio=list_bio)

@session_bp.route('/profil_recherche', methods=('GET', 'POST'))
def profil_recherche():
    nom_utilisateur = request.args.get('nom')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    return render_template('session/profil_recherche.html')

@session_bp.route('/portfolio', methods=('GET', 'POST'))
def portfolio():
    db = get_db()  # Call the function to get the database connection
    return render_template('session/portfolio.html')

@session_bp.route('/shop', methods=('GET', 'POST'))
def shop():
    db = get_db()  # Call the function to get the database connection
    return render_template('session/shop.html')

@session_bp.route('/article', methods=('GET', 'POST'))
def article():
    db = get_db()  # Call the function to get the database connection
    return render_template('session/article.html')
