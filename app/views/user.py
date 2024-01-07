from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
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

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required  
def show_profile():
    # Affichage de la page principale de l'application
    
    db = get_db()
    user_id = session.get('user_id')
    g.user = db.execute('SELECT * FROM Utilisateur WHERE IdUtilisateur = ?', (user_id,)).fetchone()
    if request.method == 'POST':
        new_username=request.form['new_username']
        new_biographie=request.form['new_biographie']
        new_email=request.form['new_email']
        old_mdp=request.form['old_mdp']
        new_mdp1=request.form['new_mdp1']
        new_mdp2=request.form['new_mdp2']
        new_compte_bancaire=request.form['new_compte_bancaire']
        type_de_compte=request.form['type_de_compte']
  
        
        if len(new_username)>=1 :
            try :
                db.execute("UPDATE Utilisateur SET NomUtilisateur = ? WHERE IdUtilisateur = ?",(new_username,user_id))
                db.commit()
            except db.IntegrityError:
                error = f"Le nom {new_username} est déjà pris."
                alert(error)
            return redirect(url_for('user.show_profile'))
        
        if len(new_biographie)>=1 :
            db.execute("UPDATE Utilisateur SET Biographie = ? WHERE IdUtilisateur = ?",(new_biographie,user_id))
        if len(new_email)>=1 :
            try :
                db.execute("UPDATE Utilisateur SET Email = ? WHERE IdUtilisateur = ?",(new_email,user_id))
                db.commit()
            except db.IntegrityError:
                error = f"L'adresse {new_email} est déjà pris."
                flash(error)
            return redirect(url_for('user.show_profile'))
        if len(new_compte_bancaire)>=1 :
            db.execute("UPDATE Utilisateur SET CompteBancaire = ? WHERE IdUtilisateur = ?",(new_compte_bancaire,user_id))
            return redirect(url_for('user.show_profile'))

        if len(old_mdp)>=1 and len(new_mdp1)>=1 and len(new_mdp2)>= 1 :
            if check_password_hash(g.user['MotDePasse'],old_mdp):
                if new_mdp1 == new_mdp2 :
                    db.execute("UPDATE Utilisateur SET MotDePasse = ? WHERE IdUtilisateur = ?",(generate_password_hash(new_mdp1),user_id))
                else : 
                    error = f"Les deux nouveaux mots de passe ne sont pas identiques"
                    flash(error)
            else :
                error = f"Mot de passe incorrect"
                flash(error)
            return redirect(url_for('user.show_profile'))
        
        if len(type_de_compte)>=1 :
            db.execute("UPDATE Utilisateur SET TypeDeCompte = ? WHERE IdUtilisateur = ?", (type_de_compte, user_id))
            db.commit()
            return redirect(url_for('user.show_profile'))
         
        #On vérifie que l'utilisateur upload un fichier
        if 'photo_de_profil' in request.files:
            file = request.files['photo_de_profil']
            if file and fichier_autorise(file.filename):
                filename = secure_filename(file.filename)
                uploads_folder = os.path.join(current_app.root_path, 'static/images/photos_profil')
                file_path = os.path.join(uploads_folder, filename)
                file.save(file_path)
                file_path_save = os.path.join('images/photos_profil/',filename)
                db.execute("UPDATE Utilisateur SET PhotoDeProfil = ? WHERE IdUtilisateur = ?", (file_path_save, user_id))
                db.commit()     
                return render_template('user/profile.html')
    return render_template('user/profile.html')



@user_bp.before_app_request
def recuperation_info_user():
    user_id = session.get('user_id')
    db = get_db()
    g.user = db.execute('SELECT * FROM Utilisateur WHERE IdUtilisateur = ?', (user_id,)).fetchone()
