from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app import login_required

session_bp = Blueprint('session', __name__,url_prefix='/session')
 
@session_bp.route('/accueil_connecte', methods=('GET', 'POST'))
@login_required
def accueil_connecte():
    username = g.user['NomUtilisateur'] if g.user else None

    return render_template('session/accueil_connecte.html',username=username) 
   