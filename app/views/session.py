from flask import (Blueprint, render_template)
from app import login_required
from app.utils import *
from app.db.db import get_db
from flask import request

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/accueil_connecte', methods=('GET', 'POST'))
@login_required
def accueil_connecte():
    list_id = [1, 2, 3, 4]

    if request.method == 'POST':
        db = get_db()
        recherche = request.form['recherche']
        # création d'une liste stockant les 10 id utilisateur dont le nom ressemble le plus à la recherche
        result = db.execute("SELECT NomUtilisateur FROM Utilisateur WHERE NomUtilisateur LIKE ? LIMIT 10", ('%' + recherche + '%',))
        list_id = [row[0] for row in result.fetchall()]

    print(list_id)
    
    return render_template('session/accueil_connecte.html', list_id=list_id)
