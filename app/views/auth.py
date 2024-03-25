from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db
import os
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_email, message, subject):
    #Information de connection
    HOST = "smtp.office365.com"
    PORT = 587
    FROM_EMAIL = r"creatorconnectbot@outlook.com"

    MDP = "TMWEB2024"

    #Information général de l'envoie
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Cc'] = FROM_EMAIL
    msg['Bcc'] = FROM_EMAIL

    #Message peut être une simple chaine de caractères pour ceci il suffit de remplacer MIMEText(message,'plain')
    msg.attach(MIMEText(message, 'html'))
    try:
        with smtplib.SMTP(HOST, port = PORT) as smtp:
            #Connection au serveur smtp
            smtp.ehlo()
            smtp.starttls()
            smtp.login(FROM_EMAIL, MDP)

            # Envoie de l'email
            smtp.send_message(msg)
            print('Email correctement envoyé')
    except Exception as e:
        print(f'Error: {e}')


# Création d'un blueprint contenant les routes ayant le préfixe /auth/...
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route /auth/register
@auth_bp.route('/register_client', methods=('GET', 'POST'))
def register_client():

    # Si des données de formulaire sont envoyées vers la route /register (ce qui est le cas lorsque le formulaire d'inscription est envoyé)
    if request.method == 'POST':

        # On récupère les champs 'username', 'password' et 'email' de la requête HTTP
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # On récupère la base de donnée
        db = get_db()

        # Si le nom d'utilisateur et le mot de passe ont bien une valeur
        # on essaie d'insérer l'utilisateur dans la base de données
        if username and password:
            try:
                # Récupérer le maximum actuel dans la colonne IdUtilisateur
                result = db.execute("SELECT MAX(IdUtilisateur) FROM Utilisateur").fetchone()
                dernier_id = result[0]

                # Vérifier si des données existent déjà
                if dernier_id is not None:
                    idUtilisateurs = dernier_id + 1
                else:
                # S'il n'y a pas de données, on commence à partir de 1 
                    idUtilisateurs = 1

                db.execute("INSERT INTO Utilisateur (NomUtilisateur, MotDePasse, Email, TypeDeCompte, IdUtilisateur, PhotoDeProfil, QrCodeTwint) VALUES (?, ?, ?, ?, ?, ?, ?)",(username, generate_password_hash(password), email, "Client", idUtilisateurs, "images/photos_profil/image_base.jpg", "images/photos_profil/image_base.jpg", "images/images_QR/Votre_QR_Code.png"))

                # db.commit() permet de valider une modification de la base de données
                db.commit()
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = f"User {username} is already registered."
                flash(error)
                return redirect(url_for("auth.register_client"))
            
            return redirect(url_for("auth.login"))
         
        else:
            error = "Username or password invalid"
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('auth/register_client.html')
    
@auth_bp.route('/register_createur', methods=('GET', 'POST'))
def register_createur():

    # Si des données de formulaire sont envoyées vers la route /register (ce qui est le cas lorsque le formulaire d'inscription est envoyé)
    if request.method == 'POST':

        # On récupère les champs 'username' et 'password' de la requête HTTP
        username = request.form['username'] 
        password = request.form['password']
        email = request.form['email']

        # On récupère la base de donnée
        db = get_db()

        # Si le nom d'utilisateur et le mot de passe ont bien une valeur
        # on essaie d'insérer l'utilisateur dans la base de données
        if username and password:
            try:
                # Récupérer le maximum actuel dans la colonne IdUtilisateur
                result = db.execute("SELECT MAX(IdUtilisateur) FROM Utilisateur").fetchone() 
                dernier_id = result[0]

                # Vérifier si des données existent déjà
                if dernier_id is not None:
                    idUtilisateurs = dernier_id + 1
                else:
                # S'il n'y a pas de données, commencer à partir de 1 par exemple
                    idUtilisateurs = 1

                db.execute("INSERT INTO Utilisateur (NomUtilisateur, MotDePasse, Email, TypeDeCompte, IdUtilisateur, PhotoDeProfil, QrCodeTwint) VALUES (?, ?, ?, ?, ?, ?, ?)",(username, generate_password_hash(password), email, "Createur", idUtilisateurs,"images/photos_profil/image_base.jpg", "images/images_QR/Votre_QR_Code.png"))
                # db.commit() permet de valider une modification de la base de données
                db.commit()
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = f"User {username} is already registered."
                flash(error)
                return redirect(url_for("auth.register_createur"))
            
            return redirect(url_for("auth.login"))
         
        else:
            error = "Username or password invalid"
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription
        return render_template('auth/register_createur.html')

# Route /auth/login
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    # Si des données de formulaire sont envoyées vers la route /login (ce qui est le cas lorsque le formulaire de login est envoyé)
    if request.method == 'POST':

        # On récupère les champs 'username' et 'password' de la requête HTTP
        username = request.form['username']
        password = request.form['password']

        # On récupère la base de données
        db = get_db()
        
        # On récupère l'utilisateur avec le username spécifié (une contrainte dans la db indique que le nom d'utilisateur est unique)
        # La virgule après username est utilisée pour créer un tuple contenant une valeur unique
        user = db.execute('SELECT * FROM Utilisateur WHERE NomUtilisateur = ?', (username,)).fetchone()

        if 'mdp_oublie' in request.form:
            print("mdp_oublie")
            mdp = "Creator1234"
            message = "Votre nouveau mot de passe est : " + mdp
            send_email(user['Email'], message, "Reinitialisation mot de passe")
            db.execute("UPDATE Utilisateur SET MotDePasse = ? WHERE IdUtilisateur = ?",(generate_password_hash(mdp), user['IdUtilisateur']))
            db.commit()

        # Si aucun utilisateur n'est trouve ou si le mot de passe est incorrect
        # on crée une variable error 
        error = None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['MotDePasse'], password):
            error = 'Incorrect password.'

        # S'il n'y pas d'erreur, on ajoute l'id de l'utilisateur dans une variable de session
        # De cette manière, à chaque requête de l'utilisateur, on pourra récupérer l'id dans le cookie session
        if error is None:
            session.clear()
            session['user_id'] = user['IdUtilisateur']
            # On redirige l'utilisateur vers la page principale une fois qu'il s'est connecté
            return redirect(url_for("session.accueil_connecte"))
        
        else:
            # En cas d'erreur, on ajoute l'erreur dans la session et on redirige l'utilisateur vers le formulaire de login
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        return render_template('auth/login.html')

# Route /auth/logout
@auth_bp.route('/logout')
def logout():
    # Se déconnecter consiste simplement à supprimer le cookie session
    session.clear()

    # On redirige l'utilisateur vers la page principale une fois qu'il s'est déconnecté
    return redirect("/")


# Fonction automatiquement appelée à chaque requête (avant d'entrer dans la route) sur une route appartenant au blueprint 'auth_bp'
# La fonction permet d'ajouter un attribut 'user' représentant l'utilisateur connecté dans l'objet 'g' 
@auth_bp.before_app_request
def load_logged_in_user():

    # On récupère l'id de l'utilisateur stocké dans le cookie session
    user_id = session.get('user_id')

    # Si l'id de l'utilisateur dans le cookie session est nul, cela signifie que l'utilisateur n'est pas connecté
    # On met donc l'attribut 'user' de l'objet 'g' à None
    if user_id is None:
        g.user = None

    # Si l'id de l'utilisateur dans le cookie session n'est pas nul, on récupère l'utilisateur correspondant et on stocke
    # l'utilisateur comme un attribut de l'objet 'g'
    else:
         # On récupère la base de données et on récupère l'utilisateur correspondant à l'id stocké dans le cookie session
        db = get_db()
        g.user = db.execute('SELECT * FROM Utilisateur WHERE IdUtilisateur = ?', (user_id,)).fetchone()


@auth_bp.route('/creation_createur_ou_client', methods=('GET', 'POST'))
def creation_createur_ou_client():
    # On récupère la base de donnée
    db = get_db 
    # à compléter
    return render_template('auth/creation_createur_ou_client.html')

@auth_bp.route('/creation_compte_createur', methods=('GET', 'POST'))
def creation_compte_createur():
    # On récupère la base de donnée
    db = get_db 
    # à compléter
    return render_template('auth/creation_compte_createur.html')  