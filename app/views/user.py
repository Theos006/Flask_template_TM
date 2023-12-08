from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from app.db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash


# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    # Affichage de la page principale de l'application
    if request.method == 'POST':
        db = get_db()
        user_id = session.get('user_id')
        new_username=request.form['new_username']
        new_biographie=request.form['new_biographie']
        new_email=request.form['new_email']
        old_mdp=request.form['old_mdp']
        new_mdp1=request.form['new_mdp1']
        new_mdp2=request.form['new_mdp2']
        new_compte_bancaire=request.form['new_compte_bancaire']
        
        if new_username is not None :
            test = db.execute("UPDATE Utilisateur SET NomUtilisateur = ? WHERE IdUtilisateur = ?",(new_username,user_id))
            db.commit()
            return redirect(url_for('user.show_profile'))
    return render_template('user/profile.html')


@user_bp.before_app_request
def recuperation_info_user():
    user_id = session.get('user_id')
    db = get_db()
    g.user = db.execute('SELECT * FROM Utilisateur WHERE IdUtilisateur = ?', (user_id,)).fetchone()




            
        
  
