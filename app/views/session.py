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
    list_img_portfolio = [] 
    list_img_shop = []
    image_portfolio = []

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
        g.nom = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom,)).fetchone()
        image_pdp = db.execute("SELECT PhotoDeProfil FROM Utilisateur WHERE NomUtilisateur = ?", (nom,))
        image_portfolio = db.execute("SELECT Image FROM ImagePortfolio WHERE IdUtilisateur = ? LIMIT 3", (g.nom['IdUtilisateur'], ))
        image_portfolio = [row[0] for row in image_portfolio.fetchall()]
        image_shop = db.execute("SELECT ImageProduit FROM Produit WHERE IdUtilisateur = ? LIMIT 3", (g.nom['IdUtilisateur'],))
        image_shop = [row[0] for row in image_shop.fetchall()]
        list_pdp.append(image_pdp.fetchone()[0])  
        if image_portfolio != None : 
            list_img_portfolio.append(image_portfolio)
        if image_shop != None :
            list_img_shop.append(image_shop)

    return render_template('session/accueil_connecte.html', list_nom=list_nom, list_pdp=list_pdp, list_img_portfolio=list_img_portfolio, list_img_shop=list_img_shop)

@session_bp.route('/profil_recherche', methods=('GET', 'POST'))
@login_required
def profil_recherche():
    nom_utilisateur = request.args.get('nom')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()

    list_reseaux = []
    reseau = db.execute('SELECT X FROM Reseaux WHERE IdUtilisateur = ?', (g.recherche['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [] and reseau != [None] :
        lien = reseau[0]
        list_reseaux.append(["X",lien])
    reseau = db.execute('SELECT Instagram FROM Reseaux WHERE IdUtilisateur = ?', (g.recherche['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [] and reseau != [None] :
        lien = reseau[0]
        list_reseaux.append(["Instagram",lien])
    reseau = db.execute('SELECT Youtube FROM Reseaux WHERE IdUtilisateur = ?', (g.recherche['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [] and reseau != [None] :
        lien = reseau[0]
        list_reseaux.append(["Youtube",lien])
    reseau = db.execute('SELECT Discord FROM Reseaux WHERE IdUtilisateur = ?', (g.recherche['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [] and reseau != [None] :
        lien = reseau[0]
        list_reseaux.append(["Discord",lien])
    reseau = db.execute('SELECT Twitch FROM Reseaux WHERE IdUtilisateur = ?', (g.recherche['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [] and reseau != [None] :
        lien = reseau[0]
        list_reseaux.append(["Twitch",lien])
    reseau = db.execute('SELECT TikTok FROM Reseaux WHERE IdUtilisateur = ?', (g.recherche['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [] and reseau != [None] :
        lien = reseau[0]
        list_reseaux.append(["Tiktok",lien])

    images_produit = db.execute('SELECT ImageProduit FROM Produit WHERE IdUtilisateur = ?', (int(g.recherche['IdUtilisateur']),))
    images_produit = [row[0] for row in images_produit.fetchall()]
    if images_produit != [] :
        images_produit.reverse()
        image_produit = images_produit[0]
    else :
        image_produit = "Rien"

    images_portfolio = db.execute('SELECT Image FROM ImagePortfolio WHERE IdUtilisateur = ?', (int(g.recherche['IdUtilisateur']),))
    images_portfolio = [row[0] for row in images_portfolio.fetchall()]
    if images_portfolio != [] :
        images_portfolio.reverse()
        image_portfolio = images_portfolio[0]
    else :
        image_portfolio = "Rien"

    print(image_portfolio)
    print(image_produit)

    return render_template('session/profil_recherche.html', nom = nom_utilisateur, list_reseaux = list_reseaux, image_portfolio = image_portfolio, image_produit = image_produit)

@session_bp.route('/portfolio', methods=('GET', 'POST'))
@login_required
def portfolio():
    nom_utilisateur = request.args.get('nom')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    images = db.execute('SELECT Image FROM ImagePortfolio WHERE IdUtilisateur = ?', (int(g.recherche['IdUtilisateur']),))
    images = [row[0] for row in images.fetchall()]
    images.reverse()
    return render_template('session/portfolio.html', images=images)

@session_bp.route('/shop', methods=('GET', 'POST'))
@login_required
def shop():
    nom_utilisateur = request.args.get('nom')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    nom_produit = db.execute('SELECT NomProduit FROM Produit WHERE IdUtilisateur = ?', (int(g.recherche['IdUtilisateur']),))
    nom_produit = [row[0] for row in nom_produit.fetchall()]
    image_produit = db.execute('SELECT ImageProduit FROM Produit WHERE IdUtilisateur = ?', (int(g.recherche['IdUtilisateur']),))
    image_produit = [row[0] for row in image_produit.fetchall()]
       
    produits=[[nom_produit[i], image_produit[i]] for i in range(len(nom_produit))]

    produits.reverse()
    
    return render_template('session/shop.html', produits=produits)
 
@session_bp.route('/article', methods=('GET', 'POST'))
@login_required
def article(): 
    nom_utilisateur = request.args.get('nom')
    nom_produit = request.args.get('nom_produit')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    g.produit = db.execute('SELECT * FROM Produit WHERE NomProduit = ? AND IdUtilisateur = ?', (nom_produit,g.recherche['IdUtilisateur'])).fetchone()
    return render_template('session/article.html', nom_produit=nom_produit)

@session_bp.route('/modification_page_publique', methods=('GET', 'POST'))
@login_required
def modification_page_publique():
    nom_utilisateur = request.args.get('nom')
    db = get_db()  
    g.user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    
    list_reseaux = []
    reseau = db.execute('SELECT X FROM Reseaux WHERE IdUtilisateur = ?', (g.user['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [None] :
        lien = reseau[0]
        list_reseaux.append(["X",lien])
    reseau = db.execute('SELECT Instagram FROM Reseaux WHERE IdUtilisateur = ?', (g.user['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [None]  :
        lien = reseau[0]
        list_reseaux.append(["Instagram",lien])
    reseau = db.execute('SELECT Youtube FROM Reseaux WHERE IdUtilisateur = ?', (g.user['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [None]  :
        lien = reseau[0]
        list_reseaux.append(["Youtube",lien])
    reseau = db.execute('SELECT Discord FROM Reseaux WHERE IdUtilisateur = ?', (g.user['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [None]  :
        lien = reseau[0]
        list_reseaux.append(["Discord",lien])
    reseau = db.execute('SELECT Twitch FROM Reseaux WHERE IdUtilisateur = ?', (g.user['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [None]  :
        lien = reseau[0]
        list_reseaux.append(["Twitch",lien])
    reseau = db.execute('SELECT TikTok FROM Reseaux WHERE IdUtilisateur = ?', (g.user['IdUtilisateur'],))
    reseau = [row[0] for row in reseau.fetchall()]
    if reseau != [None]  :
        lien = reseau[0]
        list_reseaux.append(["Tiktok",lien])

    images_produit = db.execute('SELECT ImageProduit FROM Produit WHERE IdUtilisateur = ?', (int(g.user['IdUtilisateur']),))
    images_produit = [row[0] for row in images_produit.fetchall()]
    images_produit.reverse()
    image_produit = images_produit[0]

    images_portfolio = db.execute('SELECT Image FROM ImagePortfolio WHERE IdUtilisateur = ?', (int(g.user['IdUtilisateur']),))
    images_portfolio = [row[0] for row in images_portfolio.fetchall()]
    images_portfolio.reverse()
    image_portfolio = images_portfolio[0]

    return render_template('session/modification_page_publique.html', list_reseaux = list_reseaux, image_produit = image_produit, image_portfolio = image_portfolio)

@session_bp.route('/modification_shop', methods=('GET', 'POST'))
@login_required
def modification_shop():
    nom_utilisateur = request.args.get('nom')
    db = get_db()  
    g.user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone() 
    nom_produit = db.execute('SELECT NomProduit FROM Produit WHERE IdUtilisateur = ?', (int(g.user['IdUtilisateur']),))
    nom_produit = [row[0] for row in nom_produit.fetchall()]
    image_produit = db.execute('SELECT ImageProduit FROM Produit WHERE IdUtilisateur = ?', (int(g.user['IdUtilisateur']),))
    image_produit = [row[0] for row in image_produit.fetchall()]
       
    produits=[[nom_produit[i], image_produit[i]] for i in range(len(nom_produit))]

    produits.reverse()

    image_path = request.form.get('image_path')
    if image_path:
        db = get_db()
        db.execute("DELETE FROM Produit WHERE NomProduit = ?", (image_path,))
        db.commit()
        return render_template('session/modification_shop.html', produits=produits)
    
    return render_template('session/modification_shop.html', produits=produits)


@session_bp.route('/modification_portfolio', methods=('GET', 'POST'))
@login_required
def modification_portfolio():
    nom_utilisateur = request.args.get('nom')
    db = get_db()  
    g.user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    images = db.execute('SELECT Image FROM ImagePortfolio WHERE IdUtilisateur = ?', (int(g.user['IdUtilisateur']),))
    images = [row[0] for row in images.fetchall()]
    images.reverse()
    if request.method == 'POST' :
        if 'nouvelle_image_portfolio' in request.files:
                file = request.files['nouvelle_image_portfolio']
                if file and fichier_autorise(file.filename):
                    filename = secure_filename(file.filename)
                    uploads_folder = os.path.join(current_app.root_path, 'static/images/images_portfolio')
                    file_path = os.path.join(uploads_folder, filename).replace('\\','/')
                    file.save(file_path)
                    file_path_save = os.path.join('images/images_portfolio', filename).replace('\\','/')
                    if file_path_save not in images:
                        db.execute("INSERT INTO ImagePortfolio (IdUtilisateur, Description, Image) VALUES (?,?,?)", (g.user['IdUtilisateur'], 'Description indisponible pour le moment', file_path_save))
                        db.commit()
                        return render_template('session/modification_portfolio.html', images=images)
        image_path = request.form.get('image_path')
        if image_path:
            db = get_db()
            db.execute("DELETE FROM ImagePortfolio WHERE Image = ?", (image_path,))
            db.commit()
            return render_template('session/modification_portfolio.html', images=images)
    return render_template('session/modification_portfolio.html', images=images)

@session_bp.route('/ajout_produit', methods=('GET', 'POST'))
@login_required
def ajout_produit():
    nom_utilisateur = request.args.get('nom')
    db = get_db()  
    g.user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone() 
    if request.method  == 'POST':
        nom_nouveau_produit=request.form['nom_nouveau_produit']
        description_nouveau_produit=request.form['description_nouveau_produit']
        prix_nouveau_produit=request.form['prix_nouveau_produit']

        if nom_nouveau_produit and description_nouveau_produit and prix_nouveau_produit:
            if 'photo_nouveau_produit' in request.files:
                file = request.files['photo_nouveau_produit']
                if file and fichier_autorise(file.filename):
                    filename = secure_filename(file.filename)
                    uploads_folder = os.path.join(current_app.root_path, 'static/images/images_shop')
                    file_path = os.path.join(uploads_folder, filename)
                    file.save(file_path)
                    file_path_save = os.path.join('images/images_shop/',filename)
                    db.execute("INSERT INTO Produit (IdUtilisateur, NomProduit, Prix, DescriptionProduit, ImageProduit) VALUES (?,?,?,?,?)", (g.user['IdUtilisateur'], nom_nouveau_produit, prix_nouveau_produit, description_nouveau_produit, file_path_save))
                    db.commit()
                    return render_template('session/ajout_produit.html')
    return render_template('session/ajout_produit.html')

@session_bp.route('/ajout_lien', methods=('GET', 'POST'))
@login_required
def ajout_lien():
    nom_utilisateur = request.args.get('nom')
    db = get_db()  
    g.user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone() 
    if request.method  == 'POST':
        g.reseau = db.execute('SELECT * FROM Reseaux WHERE IdUtilisateur = ?', (g.user['IdUtilisateur'],)).fetchone() 
        nom_reseau = request.form['nom_réseau']
        lien = request.form['lien']

        if g.reseau != None :
            if nom_reseau and lien :
                if nom_reseau == "X" :
                    db.execute('UPDATE Reseaux SET X = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "Instagram" :
                    db.execute('UPDATE Reseaux SET Instagram = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "Youtube" :
                    db.execute('UPDATE Reseaux SET Youtube = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "Discord" :
                    db.execute('UPDATE Reseaux SET Discord = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "Twitch" :
                    db.execute('UPDATE Reseaux SET Twitch = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "TikTok" :
                    db.execute('UPDATE Reseaux SET TikTok = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                
        else :
            if nom_reseau and lien :
                db.execute("INSERT INTO Reseaux (IdUtilisateur, X, Instagram, Youtube, Discord, Twitch, TikTok) VALUES (?,?,?,?,?,?,?)", (g.user['IdUtilisateur'], None, None, None, None, None, None))
                db.commit()
                if nom_reseau == "X" :
                    db.execute('UPDATE Reseaux SET X = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "Instagram" :
                    db.execute('UPDATE Reseaux SET Instagram = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "Youtube" :
                    db.execute('UPDATE Reseaux SET Youtube = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "Discord" :
                    db.execute('UPDATE Reseaux SET Discord = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "Twitch" :
                    db.execute('UPDATE Reseaux SET Twitch = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
                if nom_reseau == "TikTok" :
                    db.execute('UPDATE Reseaux SET TikTok = ? WHERE IdUtilisateur = ?', (lien, g.user['IdUtilisateur']))
                    db.commit()
                    return render_template('session/ajout_lien.html')
    return render_template('session/ajout_lien.html')

@session_bp.route('/qr_code', methods=('GET', 'POST'))
@login_required
def qr_code(): 
    nom_utilisateur = request.args.get('nom')
    nom_produit = request.args.get('nom_produit')
    db = get_db()
    g.recherche = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (nom_utilisateur,)).fetchone()
    print(g.recherche['QrCodeTwint'])
    g.produit = db.execute('SELECT * FROM Produit WHERE NomProduit = ? AND IdUtilisateur = ?', (nom_produit,g.recherche['IdUtilisateur'])).fetchone()
    return render_template('session/qr_code.html')

