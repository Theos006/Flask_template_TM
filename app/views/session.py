from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify)
from app.utils import *
from app.db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os

#Définition des types de fichiers autorisés afin d'éviter tout fichiers malveillants 
ALLOWED_EXTENSIONS = {'png','jpeg','jpg'}

#Fonction qui vérifie si l'extension du fichier est valide 
def fichier_autorise(fichier):
    return '.' in fichier and \
        fichier.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')


#convertiseur donnée binaire dans le bon format et le stock dans le disque 
def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/accueil_connecte', methods=('GET', 'POST'))
@login_required
def accueil_connecte():
    list_nom = ["Admin", "Mirko", "Mathieu", "Moi", "marc"]
    list_pdp = []  
    db = get_db()
    
    if request.method == 'POST':
        
        recherche = request.form['recherche']
        # création d'une liste stockant les 10 id utilisateur dont le nom ressemble le plus à la recherche
        result = db.execute(
            "SELECT NomUtilisateur FROM Utilisateur WHERE NomUtilisateur LIKE ? AND TypeDeCompte = ? LIMIT 10",
            ('%' + recherche + '%','Createur')
        )
        list_nom = [row[0] for row in result.fetchall()]
        
    for nom in list_nom:
        image = db.execute("SELECT PhotoDeProfil FROM Utilisateur WHERE NomUtilisateur = ?", (nom,))
        list_pdp.append(image.fetchone()[0])  

    print(list_nom)
    return render_template('session/accueil_connecte.html', list_nom=list_nom, list_pdp=list_pdp)

@session_bp.route('/profil_recherche', methods=('GET', 'POST'))
def profil_recherche():
    nom_utilisateur = request.args.get('nom')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    return render_template('session/profil_recherche.html', nom = nom_utilisateur)

@session_bp.route('/portfolio', methods=('GET', 'POST'))
def portfolio():
    nom_utilisateur = request.args.get('nom')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    images = db.execute('SELECT Image FROM ImagePortfolio WHERE IdUtilisateur = ?', (int(g.recherche['IdUtilisateur']),))
    images = [row[0] for row in images.fetchall()]
    return render_template('session/portfolio.html', images=images)

@session_bp.route('/shop', methods=('GET', 'POST'))
def shop():
    nom_utilisateur = request.args.get('nom')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    return render_template('session/shop.html')
 
@session_bp.route('/article', methods=('GET', 'POST'))
def article(): 
    nom_utilisateur = request.args.get('nom')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    return render_template('session/article.html')

@session_bp.route('/modification_page_publique', methods=('GET', 'POST'))
def modification_page_publique():
    nom_utilisateur = request.args.get('nom')
    print(nom_utilisateur)
    db = get_db()  
    g.user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    return render_template('session/modification_page_publique.html')

@session_bp.route('/modification_shop', methods=('GET', 'POST'))
def modification_shop():
    nom_utilisateur = request.args.get('nom')
    db = get_db()  
    g.user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone() 
    return render_template('session/modification_shop.html')

@session_bp.route('/modification_portfolio', methods=('GET', 'POST'))
def modification_portfolio():
    nom_utilisateur = request.args.get('nom')
    db = get_db()  
    g.user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    images = db.execute('SELECT Image FROM ImagePortfolio WHERE IdUtilisateur = ?', (int(g.user['IdUtilisateur']),))
    images = [row[0] for row in images.fetchall()]
    if request.method == 'POST' :
        if 'nouvelle_image_portfolio' in request.files:
                file = request.files['nouvelle_image_portfolio']
                if file and fichier_autorise(file.filename):
                    filename = secure_filename(file.filename)
                    uploads_folder = os.path.join(current_app.root_path, 'static/images/images_portfolio')
                    print(uploads_folder)
                    file_path = os.path.join(uploads_folder, filename).replace('\\','/')
                    file.save(file_path)
                    file_path_save = os.path.join('images/images_portfolio', filename).replace('\\','/')
                    if file_path_save not in images:
                        db.execute("INSERT INTO ImagePortfolio (IdUtilisateur, Description, Image) VALUES (?,?,?)", (g.user['IdUtilisateur'], 'Description indisponible pour le moment', file_path_save))
                        db.commit()
                        return render_template('session/modification_portfolio.html', images=images)
    return render_template('session/modification_portfolio.html', images=images)

@session_bp.route('/qr_code', methods=('GET', 'POST'))
def qr_code():
    db = get_db()  
    return render_template('session/qr_code.html')